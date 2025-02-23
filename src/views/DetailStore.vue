<template>
  <div class="p-2 px-3">
    <img :src="this.selectedstore[0]?.imageurl || store.image_url" alt="가게 이미지" class="w-full h-[300px] object-cover ">
    <div class="border-b-[2px]">
      <div class="flex justify-between items-center">
        <p class="text-3xl mt-2"><strong>{{ this.store.name || this.store.store_name || this.store.restaurant.name }}</strong></p>
        <div v-if="user && user.id">
          <StoreLike />
        </div>
      </div>
      <div class="flex items-center font-bold text-sm my-2">
        <p>⭐{{ this.selectedstore[0]?.rating || store.rating}}</p>
        <button @click="showreview" v-if="this.allreviews.length > 0" class="">
          <span class="text-gray-400 mx-2">·</span>
          <span>
            리뷰 {{ this.allreviews.length }}</span>개
            <i class="fa-solid fa-chevron-right"></i>
        </button>
      </div>
      <div class="my-2">
        <div v-if="allcouponstores.includes(this.store.name) || (this.store?.store_name) || allcouponstores.includes(this.store?.restaurant?.name)" class="inline-block font-bold text-xs text-violet-700 p-[3px] text-center border-1 border-violet-500 rounded-[4px]">
          <p>2000원 할인 쿠폰 발급 완료</p>
        </div>
        <div v-else class="inline-block font-bold text-xs text-violet-700 border-1 p-[3px] border-violet-500 rounded-[4px]">
          <button @click="getCoupon(2000)" class="mt-0">
            첫 주문 2000원 할인 쿠폰 받기
            <i class="fa-solid fa-download"></i>
          </button>
        </div>
      </div>
      <div class="my-1 text-sm">
        <p class="font-bold">
          운영 시간
          <span v-if="isoperatinghours(selectedstore[0]?.operatinghours).isOperating || store.operatinghours" class="ml-3">
            {{ selectedstore[0]?.operatinghours || store.operatinghours}}
          </span>
          <span v-else class="text-red-400 ml-3">
            내일 오전 {{ (isoperatinghours(selectedstore[0]?.operatinghours)).nextStart}} 오픈
          </span>
        </p>
      </div>
    </div>

    <div v-if="menus.length > 0" class="my-3">
      <div v-if="storeReview && allreviews.length > 0">
        <AllReviews :cancel="closereview" :reviews="this.allreviews"/>
      </div>
      <p class="text-xl"><strong>메뉴</strong></p>
      <div v-for="menu in menus" :key="menu.id" class="border-b-[1px]">
        <div class="flex justify-between py-3">
          <div class="basis-3/4 py-2 px-1">
            <p class="text-lg font-bold pb-2">{{ menu.name }}</p>
            <p class="text-sm pb-2">{{ menu.description }}</p>
            <p class="text-sm font-bold">{{ menu.price.toLocaleString() }}원</p>
            <!--옵션 그룹이 있을 경우 출력-->
            <div v-if="menu.option_groups && menu.option_groups.length > 0">
              <div v-for="optionGroup in menu.option_groups" :key="optionGroup.group_name" class="mt-3 text-sm">
                <p class="font-bold">추가 옵션</p>
                <ul class="list-disc ml-5">
                  <li v-for="optionItem in optionGroup.items" :key="optionItem.name">
                    <p>{{ optionItem.name }} : <span class="font-bold">{{ optionItem.price.toLocaleString() }}원</span></p>
                  </li>
                </ul>
              </div>
            </div>
            <button @click="showMessage(menu)" class="border-1 px-[5px] py-[3px] border-violet-500 rounded-[4px] text-violet-700 text-xs font-bold my-3">
              장바구니 담기
              <i class="fa-solid fa-plus"></i>
            </button>
          </div>
          <div>
            <img v-if="menu.image_url" :src="menu.image_url" alt="Menu Image" class="w-[300px] h-[200px] rounded-md">
          </div>
        </div>
      </div>

      <div v-if="addtocart" class="transition-opacity duration-500 fixed bg-black text-white text-sm rounded-md shadow-lg py-2 px-3 transform -translate-x-1/2 -translate-y-1/2 top-1/3 left-1/2" :class="{'opacity-0': !addtocart}">
        <p>장바구니에 메뉴를 추가했습니다.</p>
      </div>

      <div v-if="!isSameStore" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
        <div class="absolute bg-white w-[300px] h-[181px] rounded-sm shadow-lg transform -translate-x-1/2 -translate-y-1/2 top-1/2 left-1/2">
          <div class="pt-4 px-4">
            <p class="font-bold text-center mb-3 text-sm">장바구니에는 같은 가게의 메뉴만 담을 수 있습니다.</p>
            <p class="text-xs text-gray-400 text-center pb-4">선택하신 메뉴를 장바구니에 담을 경우 이전에 담은 메뉴가 삭제됩니다.</p>
          </div>
          <div class="w-full flex h-[45px] border-t">
            <button @click="closeMessage" class="basis-1/2 border-r">취소</button>
            <button @click="addCart(addmenu)" class="basis-1/2">담기</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="menucart.length > 0">
      <button @click="gotoMyCart(this.menucart)" class="border-1 px-[5px] py-[3px] border-violet-500 rounded-[4px] text-violet-700 text-sm font-bold my-3">{{ totalPrice }}원 - 주문하기 {{ this.menucart.length }}</button>
    </div>

    <!-- 옵션 팝업 -->
    <div v-if="showPopup" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
      <div class="bg-white p-4 rounded-lg w-4/5 max-w-md">
        <div class="flex justify-between">
          <p class="font-bold">추가 옵션 선택</p>
          <button @click="closePopup" class="px-[5px] py-[3px] rounded-[4px] text-xs font-bold ml-2">
            <i class="fa-solid fa-x"></i>
          </button>
        </div>
        <div v-for="(group, index) in optiongroups" :key="index" class="mt-2">
          <div v-for="(item, i) in group.items" :key="i">
            <label>
              <input 
                type="checkbox" 
                :value="i" 
                :name="group.group_name" 
                @change="toggleOption(item)"
              />
              <span class="text-sm ml-2">{{ item.name }} <span class="font-bold">(+{{ item.price }}원)</span></span>
            </label>
          </div>
          <label class="text-sm"><input type="checkbox"> {{ "선택 안함" }} <span class="font-bold">(+0원)</span></label>
        </div>
        <div class="mt-2">
          <button @click="addToCartWithOptions" class="border-1 px-[5px] py-[3px] border-violet-500 rounded-[4px] text-violet-700 text-xs font-bold mt-2">담기</button>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios';
import AllReviews from '../components/AllReviews.vue'
import StoreLike from '../components/StoreLike.vue'
import { mapGetters } from 'vuex';
import { isOperatingHour } from '../utils/isoperatinghours.js';

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
      allcouponstores: [],
      likedstore: [],
      selectedstore: [],
      isSameStore: true,
      addmenu: [],
      addtocart: false
    }
  },
  components: {
    AllReviews,
    StoreLike
  },
  computed: {
    ...mapGetters(['getLikedStore']),
    store() {
      return this.$store.getters.getStore;
    },
    user() {
      return this.$store.getters.getUser;
    },
    totalPrice() {
      console.log('현재 menucart:', this.menucart); // 로그 추가
      return this.menucart.reduce((total, menu) => total + menu.price, 0).toLocaleString();
    },
    menu() {
      return this.$store.getters.getMenuCart
    }
  },
  mounted() {
    this.getMenus(this.store.id || this.store.store_id || this.store.restaurant.id);
    this.AllReviews();
    this.likedstore = this.getLikedStore;
    if (this.user && this.user.id) {
      this.getAllCoupons();
    }
    this.getStoredata();
  },
  methods: {
    async getMenus(storeid) {
      const response = await axios.get(`http://localhost:8000/order/getmenus/${storeid}/`)
      this.menus = response.data
    },
    addCart(menu) {
      this.isSameStore = true;
      if (this.user && this.user.id) {
        if (menu.option_groups && menu.option_groups.length > 0) {
          // 만약 메뉴에 옵션이 있을 경우 옵션 팝업 열기
          this.openPopup(menu.option_groups, menu)
        } else { // 옵션이 없는 메뉴라면 바로 장바구니에 추가
          this.showAddToCartMessage();
          this.menucart.push({
            ...menu, 
            'storeid': this.store.id, 'storename': this.store.name
          })
          this.$store.commit('setMenucart', this.menucart);

          console.log('단일 메뉴', this.menucart);
        }
      } else {
        alert("로그인이 필요한 서비스입니다.");
        this.$router.push('/login');
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
      this.showAddToCartMessage();
      this.closePopup();
      this.$store.commit('setMenucart', this.menucart);
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
      console.log('gotoMyCart의 메뉴', menucart);

      console.log(this.store);
      if (this.store) {
        this.$router.push('/mycart');
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
    async getAllCoupons() { // 발급받은 모든 쿠폰 가져오기
      try {
        const response = await axios.get(`http://localhost:8000/order/getallcoupons/${this.user.id}/`)

        this.allcoupons = response.data.coupons;  // 응답에서 coupons 배열만 사용
        this.allcouponstores = this.allcoupons.map(coupon => coupon.store); // store만 모아서 배열에 저장
        console.log(this.allcouponstores);  // 확인용 출력
      } catch (error) {
        console.error('Error fetching coupon:', error);
      }
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
        this.getAllCoupons();
      } catch (error) {
        console.error('Error fetching coupon:', error);
      }
    },
    async getStoredata() {
      const response = await axios.get("http://localhost:8000/order/getallstores/");
      console.log('모든 가게들', response.data);

      this.selectedstore = response.data.filter((store) => store.id === this.store.id);
      console.log('현재 가게', this.selectedstore);
    },
    isoperatinghours(hour) {
      return isOperatingHour(hour);
    },
    showMessage(menu) {
      console.log(menu.price);
      console.log('현재 메뉴가 있는지', this.menu[0]?.storeid);
      console.log('현재 가게', this.store.id);
      if (this.menu[0]?.storeid !== undefined && this.menu[0]?.storeid !== this.store.id) {
        this.isSameStore = false;
        this.addmenu = menu
      } else {
        this.addCart(menu);
      }
    },
    closeMessage() {
      this.isSameStore = true
    },
    showAddToCartMessage() {
      this.addtocart = true;
      setTimeout(() => {
        this.addtocart = false; 
      }, 3000); 
    }
  }
}
</script>
