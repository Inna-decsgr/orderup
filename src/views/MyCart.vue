<template>
  <div>
    <h5>장바구니</h5>
    <button @click="clearcart">장바구니 비우기</button>
    <p v-if="couponCount">사용 가능한 쿠폰이 {{couponCount}}개 있습니다.</p>
    <div v-if="menucart.length === 0">
      <p>장바구니가 텅 비었어요</p>
      <button @click="gotoHome">+더 담으러 가기</button>
    </div>
    <div v-else>
      <p v-if="store"><strong>{{ store.name || store.store_name }}</strong></p>
      <div v-for="(item, index) in menucart" :key="index" class="menu-item">
        <strong>{{ item.menu ? item.menu.name : item.name}}</strong>
        <p>가격: {{ item.menu ? item.menu.price.toLocaleString() : item.price.toLocaleString() }}원</p>

        <!--옵션 그룹이 있는 경우 옵션 출력-->
        <div v-if="item.menu && Array.isArray(item.menu.option_groups) && item.menu.option_groups.length > 0">
          <ul>
            <span v-for="(group, groupIndex) in item.menu.option_groups" :key="groupIndex">
              <p v-for="(option, optionIndex) in group.items" :key="optionIndex">
                {{ option.name }} (+{{ option.price.toLocaleString() }}원)
              </p>
            </span>
          </ul>
        </div>

        <p v-if="item.menu && item.menu.option_groups">
          {{ 
            (item.menu 
            ? ( 
              item.menu.price + (item.menu.option_groups ? item.menu.option_groups.reduce((acc, group) => {return acc + group.items.reduce((groupAcc, option) => { return groupAcc + (item.options && item.options[option.name] ? item.options[option.name] : 0);
              }, 0);
            }, 0)
            : 0)) : item.price).toLocaleString()
          }}원
        </p>
      </div>

      <div>
        <label v-if="couponCount">
          <input type="checkbox" v-model="showDiscount" />
          {{this.discount}}원 쿠폰 적용하기
        </label>
      </div>

      <div>
        <p>
          {{ (Number(this.deliveryfee) + Number(this.totalCartPrice)).toLocaleString()}}원
        </p>
        <p>배달비 : {{ this.deliveryfee || store.delivery_fee }}원</p>
        <p v-if="showDiscount">
          - {{ Number(this.discount).toLocaleString() }}원
        </p>
        <p>총 금액 : {{ (Number(this.deliveryfee || store.delivery_fee) + Number(this.totalCartPrice) - (this.showDiscount ? Number(this.discount) : 0)).toLocaleString()}}원</p>
      </div>
    
      <!--주문 총 금액-->
      <button @click="removemenu"><i class="fa-solid fa-trash"></i></button>
      <button @click="openPopup">주문하기</button>


      <div v-if="showPopup" class="popup">
        <div class="popup-content">
          <button @click="closePopup">닫기</button>
          <form @submit.prevent="handlePayment">
            <h3>결제 정보 입력</h3>
            <div>
              <label for="cardNumber">카드 번호</label>
              <input 
                type="text" 
                id="cardNumber" 
                v-model="paymentDetails.cardNumber"
                placeholder="카드 번호"
                required
              />
            </div>
            <div>
              <label for="cardNumber">유효 기간</label>
              <input 
                type="text" 
                id="expiryDate" 
                v-model="paymentDetails.expiryDate"
                placeholder="MM/YY"
                required
              />
            </div>
            <div>
              <label for="cardNumber">CVV</label>
              <input 
                type="text" 
                id="cvv" 
                v-model="paymentDetails.cvv"
                placeholder="CVV"
                required
              />
            </div>
            <div>
              <p>총 금액: {{ (Number(this.deliveryfee) + Number(this.totalCartPrice) - (this.showDiscount ? Number(this.discount) : 0)).toLocaleString()}} 원</p>
            </div>
            <button type="submit">결제하기</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      showPopup: false,
      paymentDetails: {
        cardNumber: '',
        expiryDate: '',
        cvv: '',
      },
      totalPrice: '',
      deliveryfee: '',
      allcouponstores: [],
      discount: '',
      showDiscount: false
    }
  },
  computed: {
    menucart() {
      return this.$store.state.menucart;
    },
    totalCartPrice() {
      return this.menucart.reduce((total, item) => {
        let itemTotalPrice = item.menu ? item.menu.price : item.price; // 메뉴의 기본 가격 설정

        // 메뉴가 있고 옵션 그룹이 있을 경우 옵션 가격 추가
        if (item.menu && item.menu.option_groups) {
          item.menu.option_groups.forEach(group => {
            group.items.forEach(option => {
              // 선택된 옵션이 있는 경우 해당 가격 추가
              if (item.options && item.options[option.name]) {
                itemTotalPrice += item.options[option.name];
              }
            });
          });
        }

        // 각 항목의 총 가격을 누적해서 합산
        return total + itemTotalPrice;
      }, 0);
    },
    store() {
      return this.$store.getters.getStore;
    },
    user() {
      return this.$store.getters.getUser;
    },
    couponCount() {
      return this.allcouponstores.filter(coupon => coupon.store_id === this.store.id && coupon.is_used === false).length;
    }
  },
  mounted() {
    this.getDeliveryfee(this.store.id);
    this.showStoreCoupon();
  },
  methods: {
    async handlePayment() {
      console.log('결제 정보:', this.paymentDetails);
      alert('결제가 완료되었습니다!');

      // 데이터베이스에 주문 메뉴와 결제 정보 저장하는 로직 구현
      const orderData = {
        items: this.menucart.map(item => {
          // 선택한 옵션만 포함한 객체 생성
          const selectedOptions = [];

          // 메뉴의 option_groups이 존재하는지 확인
          if (item.menu && item.menu.option_groups) {
            console.log("현재 메뉴 옵션 그룹:", item.menu.option_groups);

            // 각 옵션 그룹을 순회
            item.menu.option_groups.forEach(group => {
              // 옵션 그룹의 항목을 그대로 options에 넣기
              if (group.items && group.items.length > 0) {
                group.items.forEach(option => {
                  // item.options에서 해당 option의 이름을 찾아서 그 가격을 추가
                  if (item.options && item.options[option.name]) {
                    selectedOptions.push({
                      name: option.name,
                      price: item.options[option.name]
                    });
                  }
                });
              }
            });
          }

          // 선택된 옵션이 없으면 빈 배열로 처리
          const finalOptions = selectedOptions.length > 0 ? selectedOptions : [];

          return {
            menu_id: item.menu ? item.menu.id : item.id,
            name: item.menu ? item.menu.name : item.name,
            options: finalOptions,
            price: item.menu ? item.menu.price : item.price
          };
        }),

        user_coupon_id: this.discount ? this.user.id : null,

        restaurant_id: this.store.id,
        paymentDetails: {
          cardNumber: this.paymentDetails.cardNumber,
          expiryDate: this.paymentDetails.expiryDate,
          cvv: this.paymentDetails.cvv
        },
        totalAmount: this.totalCartPrice,
        discount_amount : this.discount ? Number(this.discount) : 0
      }
      console.log('요청 데이터', orderData);
      console.log(this.store.id);

      const csrfResponse = await axios.get("http://localhost:8000/order/csrftoken/");
      const csrfToken = csrfResponse.data.csrfToken;


      const response = await axios.post('http://localhost:8000/order/addorder/', orderData, {
        headers: {
          'X-CSRFToken': csrfToken,
        }
      });
      console.log(response.data);
      this.closePopup();
      this.$router.push('/orderlist');
    },
    openPopup() {
      this.showPopup = true;
      console.log('주문한 메뉴', this.menucart);
    },
    closePopup() {
      this.showPopup = false
    },
    gotoHome() {
      this.$router.push('/');
    },
    removemenu() {
      this.$store.commit('clearMenucart');
    },
    async getDeliveryfee(storeid) {
      const stores = await axios.get('http://localhost:8000/order/getallstores/');
      console.log(stores.data);

      const store = stores.data.find(store => store.id === storeid);

      if (store && store.deliveryfee) {
        this.deliveryfee = store.deliveryfee;
        console.log(this.deliveryfee);
      } else {
        console.error('Store or delivery fee not found');
      }
    },
    clearcart() {
      this.$store.commit('clearMenucart');
    },
    async showStoreCoupon() {
      const response = await axios.get(`http://localhost:8000/order/getallcoupons/${this.user.id}/`)

      this.allcouponstores = response.data.coupons; // store만 모아서 배열에 저장
      console.log(response.data.coupons);
      this.discount = response.data.coupons.find(coupon => coupon.store_id === this.store.id && coupon.is_used == 'false')?.discount_amount;
      console.log(this.discount || null);
    }
  }
}
</script>


<style>
ul {
  list-style: none;
  padding-left: 0 !important;
  margin: 0;
}

.popup {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.popup-content {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  width: 80%;
  max-width: 500px;
}

</style>