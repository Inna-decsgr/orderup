<template>
  <div class="p-2 px-3">
    <p class="font-bold text-center text-xl">장바구니</p>
    <div v-if="menucart.length === 0" class="flex flex-col justify-center items-center absolute top-[45%] left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <img src="/media/images/cart dog.png" alt="장바구니 이미지" class="w-[150px]" />
      <p class="font-bold pt-4 pb-3">장바구니가 텅 비었어요</p>
      <button @click="gotoHome" class="border py-1 px-2 rounded-3xl">
        <i class="fa-solid fa-plus text-gray-500"></i>
        <span class="text-sm font-bold"> 더 담으러 가기</span>
      </button>
    </div>
    <div v-else>
      <div class="flex items-center cursor-pointer py-2" @click="gotoStoreDetail(store)">
        <img :src="selectedstore[0]?.imageurl" alt="가게 이미지" class="w-[30px] h-[30px] rounded-lg" />
        <p v-if="store" class="font-bold px-2">
          {{ store.name || store.store_name }}
        </p>
        <i class="fa-solid fa-chevron-right"></i>
      </div>
      <div v-for="(item, index) in menucart" :key="index" class="border rounded-md p-3 flex items-center justify-between mb-2">
        <div>
          <p class="font-bold">{{ item.menu ? item.menu.name : item.name}}</p>
          <p class="text-gray-500">가격: {{ item.menu ? item.menu.price.toLocaleString() : item.price.toLocaleString() }}원</p>

          <!--옵션 그룹이 있는 경우 옵션 출력-->
          <div v-if="item.options && Object.keys(item.options).length > 0">
            <ul class="text-gray-500">
              <li v-for="([name, price], index) in Object.entries(item.options)" :key="index">
                {{ name }} (+{{ price.toLocaleString() }}원)
              </li>
            </ul>
          </div>

          <p v-if="item.menu && item.options" class="font-bold my-2">
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
        <div class="pr-5">
          <button @click="removemenu(item.id)"><i class="fa-solid fa-trash"></i></button>
        </div>
      </div>
      
      <div class="pt-3">
        <p class="font-bold pb-2">결제금액을 확인해주세요</p>
        <div class="border rounded-md p-3">
          <div>  
            <div class="flex items-center space-x-2">
              <label v-if="couponCount" class="flex items-center space-x-2">
                <p v-if="couponCount" class="bg-violet-50 border-1 border-violet-200 py-1 px-2 text-xs font-bold text-violet-500 rounded-md mb-1">사용 가능한 쿠폰이 {{couponCount}}개 있습니다.</p>
                <input type="checkbox" v-model="showDiscount"/>
                <span class="text-xs">{{this.discount}}원 쿠폰 적용하기</span>
              </label>
            </div>
            <div class="flex justify-between font-bold">
              <p class="text-sm mt-2">총 금액</p>
              <p> {{ Number(this.totalCartPrice).toLocaleString()}}원</p>
            </div>
            <div class="flex justify-between text-xs text-gray-400 font-bold mt-2">
              <p>주문금액</p>
              <p>{{ Number(this.totalCartPrice).toLocaleString()}}원</p>
            </div>
            <div class="flex justify-between border-b text-xs text-gray-400 font-bold mt-2 pb-2">
              <p>배달팁</p>
              <p>{{ this.deliveryfee.toLocaleString() }}원</p>
            </div>
            <div v-if="this.showDiscount" class="flex justify-between text-xs text-gray-400 font-bold mt-2">
              <p>할인쿠폰</p>
              <p>- {{ Number(this.discount).toLocaleString() }}원</p>
            </div>
            <div class="flex justify-between text-sm pt-2 font-bold">
              <p>결제예정금액</p>
              <p>{{ (Number(this.deliveryfee || store.delivery_fee) + Number(this.totalCartPrice) - (this.showDiscount ? Number(this.discount) : 0)).toLocaleString()}}원</p>
            </div>
          </div>
        </div>
        <p class="text-xs my-2 text-gray-400 font-bold">(주)오더업은 통신판매중개자이며, 통신판매의 당사자가 아닙니다. 따라서 (주)오더업은 상품, 거래정보 및 거래에 대하여 책임을 지지 않습니다.</p>
        <button @click="openPopup" class="bg-violet-400 w-full p-2 text-white font-bold my-3 rounded-sm">주문하기</button>
      </div>


      <div v-if="showPopup" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
        <div class="absolute bg-white w-[350px] h-[350px] rounded-md p-4 shadow-lg transform -translate-x-1/2 -translate-y-1/2 top-1/2 left-1/2">
          <div class="flex justify-between items-center pb-3">
            <p class="font-bold text-lg">결제 정보 입력</p>
            <button @click="closePopup">
              <i class="fa-solid fa-x"></i>
            </button>
          </div>
          <form @submit.prevent="handlePayment">
            <div class="mb-2 text-sm">
              <label for="cardNumber" class="font-bold w-[80px] text-center">카드 번호</label>
              <input 
                type="text" 
                id="cardNumber" 
                v-model="paymentDetails.cardNumber"
                placeholder="카드 번호"
                required
                class="border ml-4 rounded-sm p-1"
              />
            </div>
            <div class="mb-2 text-sm">
              <label for="cardNumber" class="font-bold w-[80px] text-center">유효 기간</label>
              <input 
                type="text" 
                id="expiryDate" 
                v-model="paymentDetails.expiryDate"
                placeholder="MM/YY"
                required
                class="border ml-4 rounded-sm p-1"
              />
            </div>
            <div class="mb-4 text-sm border-b pb-4">
              <label for="cardNumber" class="font-bold w-[80px] text-center">CVV</label>
              <input 
                type="text" 
                id="cvv" 
                v-model="paymentDetails.cvv"
                placeholder="CVV"
                required
                class="border ml-4 rounded-sm p-1"
              />
            </div>
            <div class="flex justify-between items-center font-bold">
              <p>총 결제금액</p>
              <p>{{ (Number(this.deliveryfee) + Number(this.totalCartPrice) - (this.showDiscount ? Number(this.discount) : 0)).toLocaleString()}} 원</p>
            </div>
            <button type="submit" class="bg-violet-400 w-full p-1 text-white font-bold my-3 rounded-sm">결제하기</button>
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
      showDiscount: false,
      selectedstore: []
    }
  },
  computed: {
    menucart() {
      return this.$store.getters.getMenuCart;
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
    },
  },
  mounted() {
    this.getDeliveryfee(this.store.id);
    this.showStoreCoupon();
    this.getStoredata();
    console.log('MyCart에서 불러온 menucart', this.menucart);
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
    removemenu(itemid) {
      console.log('장바구니에서 삭제할 메뉴 아이디', itemid);
      this.$store.commit('removeMenuItem', itemid);
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
    async showStoreCoupon() {
      const response = await axios.get(`http://localhost:8000/order/getallcoupons/${this.user.id}/`)

      this.allcouponstores = response.data.coupons; // store만 모아서 배열에 저장
      console.log(response.data.coupons);
      console.log('가게 아이디',this.store.id);
      this.discount = response.data.coupons.find(coupon => Number(coupon.store_id) === Number(this.store.id) && coupon.is_used === false)?.discount_amount;
      console.log('할인 금액', this.discount);
    },
    async getStoredata() {
      const response = await axios.get("http://localhost:8000/order/getallstores/");
      console.log('모든 가게들', response.data);

      this.selectedstore = response.data.filter((store) => store.id === this.store.id);
      console.log('현재 가게', this.selectedstore);
    },
    gotoStoreDetail(store) {
      this.$router.push('/detailstore');
      this.$store.commit('setStore', store);
    }
  }
}
</script>
