<template>
  <div>
    가게 상세 페이지
    <h5><strong>{{ this.store.name || this.store.store_name || this.store.restaurant.name }}</strong></h5>
    <div v-if="menus.length > 0">
      <button @click="showreview">리뷰 <span>{{ this.allreviews.length }}</span>개</button>
      <div v-if="allcouponstores.includes(this.store.name) || (this.store?.store_name) || allcouponstores.includes(this.store?.restaurant?.name)">
        <p>2000원 할인 쿠폰 발급 완료</p>
      </div>
      <div v-else>
        <button @click="getCoupon(2000)">첫 주문 2000원 할인 쿠폰 받기</button>
      </div>
      <div v-if="storeReview && allreviews.length > 0">
        <AllReviews :cancel="closereview" :reviews="this.allreviews"/>
      </div>
      <p><strong>메뉴판</strong></p>
      <div v-for="menu in menus" :key="menu.id">
        <p>{{ menu.name }}</p>
        <p>{{ menu.description }}</p>
        <p>{{ menu.price.toLocaleString() }}원</p>
        <img v-if="menu.image_url" :src="menu.image_url" alt="Menu Image" style="width: 400px; height: 300px;">
        <!--옵션 그룹이 있을 경우 출력-->
        <div v-if="menu.option_groups && menu.option_groups.length > 0">
          <div v-for="optionGroup in menu.option_groups" :key="optionGroup.group_name">
            <p>{{ optionGroup.group_name }}</p>
            <ul>
              <li v-for="optionItem in optionGroup.items" :key="optionItem.name">
                {{ optionItem.name }} - {{ optionItem.price }} 원
              </li>
            </ul>
          </div>
        </div>
        <button @click="addCart(menu)">{{ menu.price.toLocaleString() }}원 담기</button>
      </div>
    </div>

    <div v-if="menucart.length > 0">
      <button @click="gotoMyCart(this.menucart)">{{ totalPrice }}원 - 주문하기 {{ this.menucart.length }}</button>
    </div>

    <!-- 옵션 팝업 -->
    <div v-if="showPopup" class="popup">
      <div class="popup-content">
        <h3>옵션 선택</h3>
        <div v-for="(group, index) in optiongroups" :key="index">
          <h4>{{ group.group_name }}</h4>
          <div v-for="(item, i) in group.items" :key="i">
            <label>
              <input 
                type="checkbox" 
                :value="i" 
                :name="group.group_name" 
                @change="toggleOption(item)"
              />
              {{ item.name }} (+{{ item.price }}원)
            </label>
          </div>
          <label><input type="checkbox"> {{ "선택 안함" }} (+0원)</label>
        </div>
        <button @click="addToCartWithOptions">담기</button>
        <button @click="closePopup">닫기</button>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios';
import AllReviews from '../components/AllReviews.vue'

export default {
  data() {
    return {
      menus: [],
      menucart: [],
      showPopup: false,
      selectedMenu: [],
      selectedOptions: {},
      optiongroups: [],
      storeReview: false,
      allreviews: [],
      allcoupons: [],
      allcouponstores: []
    }
  },
  components: {
    AllReviews
  },
  computed: {
    store() {
      return this.$store.getters.getStore;
    },
    user() {
      return this.$store.getters.getUser;
    },
    totalPrice() {
      return this.menucart.reduce((total, menu) => total + menu.price, 0).toLocaleString();
    }
  },
  mounted() {
    this.getMenus(this.store.id || this.store.store_id || this.store.restaurant.id);
    this.AllReviews();
    this.getAllCoupons();
  },
  methods: {
    async getMenus(storeid) {
      const response = await axios.get(`http://localhost:8000/order/getmenus/${storeid}/`)
      this.menus = response.data
    },
    addCart(menu) {
      if (menu.option_groups && menu.option_groups.length > 0) {
        // 만약 메뉴에 옵션이 있을 경우 옵션 팝업 열기
        this.openPopup(menu.option_groups, menu)
      } else { // 옵션이 없는 메뉴라면 바로 장바구니에 추가
        alert('장바구니에 메뉴가 추가되었습니다.');
        this.menucart.push({ ...menu })
        console.log('단일 메뉴', this.menucart);
      }
    },
    openPopup(optiongroups, menu) {
      // 팝업 열고, 옵션 그룹과 메뉴 저장
      this.selectedMenu = menu;  // 장바구니에 담을 메뉴 selectedMenu에 저장
      this.optiongroups = optiongroups; // 옵션이 있는 메뉴일 경우 전달받은 옵션 그룹을 optiongroups에 저장
      this.showPopup = true  // 팝업 열기
    },
    closePopup() {
      this.showPopup = false  // 팝업 닫기
    },
    addToCartWithOptions() {
      // 옵션 선택한 후 장바구니에 추가
      const cartItem = {
        menu: this.selectedMenu,  // cartItem의 menu에는 현재 선택된 메뉴 저장
        options: this.selectedOptions,  // options에는 현재 선택된 메뉴의 옵션 중 사용자가 추가한 옵션 아이템들을 저장
        price: this.calculateTotalPrice()  // 선택된 메뉴의 가격에 만약 옵션이 추가된 경우 옵션 가격까지 더한 값을 price에 저장
      };
      this.menucart.push(cartItem);
      alert('장바구니에 메뉴가 추가되었습니다.');
      this.closePopup();
      console.log('옵션 추가된 메뉴', this.menucart);
    },
    toggleOption(item) {
      // 선택한 옵션이 이미 'selectedOptions'에 있는지 확인
      if (this.selectedOptions[item.name]) {
        // 이미 선택된 옵션이라면 'selectedOptions'에서 제거
        delete this.selectedOptions[item.name];
      } else {
        // 선택되지 않은 옵션이라면 'selectedOptions'에 추가
        this.selectedOptions[item.name] = item.price;
      }
    },
    calculateTotalPrice() {
      // 메뉴 기본 가격에 선택된 옵션 가격 더하기
      let totalPrice = this.selectedMenu.price;

      // 선택된 옵션에 대한 가격 추가
      for (const optionPrice of Object.values(this.selectedOptions)) {
        totalPrice += optionPrice;
      }
      return totalPrice;
    },
    gotoMyCart(menucart) {
      this.$store.commit('setMenucart', menucart);

      console.log(this.store);
      if (this.store) {
        this.$router.push({
          path: '/mycart',
          query: {
          store: JSON.stringify(this.store)  // store를 문자열로 변환하여 넘겨줍니다.
          }
        });
      }
    },
    async AllReviews() {
      try {
        const response = await axios.get(`http://localhost:8000/order/allreviews/${this.store.id || this.store.store_id || this.store.restaurant.id}`);
        console.log(response.data);
        this.allreviews = response.data.reviews;
        console.log('리뷰 개수', this.allreviews.length);
      } catch (error) {
        console.error('Error fetching reviews:', error);
      }
    },
    showreview() {
      this.storeReview = true
    },
    closereview() {
      this.storeReview = false
    },
    async getCoupon(discountamount) { // 쿠폰 발급받기
      try {
        const csrfResponse = await axios.get("http://localhost:8000/order/csrftoken/");
        const csrfToken = csrfResponse.data.csrfToken;

        const response = await axios.post(`http://localhost:8000/order/getcoupon/${this.user.id}/`, { storeid: this.store.id, discount_amount : discountamount }, {
          headers: {
            'X-CSRFToken': csrfToken,  
          }
        })
        console.log('쿠폰 발급받기', response.data);
        this.coupon = response.data;
      } catch (error) {
        console.error('Error fetching coupon:', error);
      }
    },
    async getAllCoupons() { // 발급받은 모든 쿠폰 가져오기
      try {
        const response = await axios.get(`http://localhost:8000/order/getallcoupons/${this.user.id}/`)
        console.log('해당 가게에서 발급받은 모든 쿠폰 가져오기', response.data);

        this.allcoupons = response.data.coupons;  // 응답에서 coupons 배열만 사용
        this.allcouponstores = this.allcoupons.map(coupon => coupon.store); // store만 모아서 배열에 저장
        console.log(this.allcouponstores);  // 확인용 출력
      } catch (error) {
        console.error('Error fetching coupon:', error);
      }
    },
  }
}
</script>

<style scoped>
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
}

.popup-content {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  width: 80%;
  max-width: 500px;
}

button {
  margin-top: 10px;
}
</style>