<template>
  <div class="p-3">
    <div>
      <div class="flex justify-between items-center pb-3">
        <div>
          <button @click="goHome"><i class="fa-solid fa-arrow-left"></i></button>
          <span class="ml-3"><strong>음식 배달 🍴</strong></span>
        </div>
        <button v-if="user" @click="gotoMyCart" class="mr-2">
          <i class="fa-solid fa-cart-shopping"></i>
        </button>
      </div>
      <p class="font-bold text-sm">{{ user.address }}</p>
      <div class="my-3">
        <swiper slides-per-view="5" class="my-swiper">
          <swiper-slide 
            v-for="(category, index) in categories" 
            :key="index" 
            @click="categoryStore(category)" 
            class="w-[80px] h-[80px] text-[13px] font-bold text-center border-b-2"
          >
            <button class="w-24 h-[80px]" :class="this.selectedcategory.name === category.name ? 'border-b-[3px] border-black' : 'border-transparent'">
              <span class="text-3xl">{{ category.icon }}</span>
              <p class="mt-2">{{ category.name }}</p>
            </button>
          </swiper-slide>
        </swiper>
      </div>
    </div>
    <div v-if="filteredstore && filteredstore.length">
      <div v-for="store in filteredstore" :key="store.id" @click="detailstore({id:store.id, name: store.name})" class="cursor-pointer mb-4">
        <swiper slides-per-view="3" class="my-swiper">
          <swiper-slide
            v-for="menu in store.menus" 
            :key="menu.id"
            class="relative mx-[1px]"
          >
            <div class="absolute text-xs bg-gradient-to-b from-black/70 via-black/50 to-transparent p-[7px] text-white w-full rounded-t-md">
              <p>{{ menu.name }}</p>
              <p class="font-bold">{{ Number(menu.price).toLocaleString() }}원</p>
            </div>
            <img :src="menu.imageurl" :alt="menu.name + ' 이미지'" class="w-[150px] h-[150px]">
          </swiper-slide>
        </swiper>
        <p v-if="!allcouponstores.includes(store.name)" class="font-bold text-xs text-violet-700 w-[110px] h-[18px] text-center my-[6px] border-1 border-violet-500 rounded-[4px]">첫 주문 할인 쿠폰</p>
        <div class="flex items-center font-bold mt-1">
          <h3 class="text-md">{{ store.name }}</h3>
          <p class="ml-1">⭐{{ store.rating }}</p>
        </div>
        <div class="flex">
          <p class="text-[13px]">{{ store.address }}</p>
          <p class="text-[13px] ml-4">{{ store.phonenumber }}</p>
        </div>
        <p class="text-xs mt-1">배달팁 💸 <span class="font-bold">{{ store.deliveryfee }}원</span></p>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import axios from 'axios';
import { Swiper, SwiperSlide } from 'swiper/vue';

export default {
  data() {
    return {
      likedstore: [],
      allcouponstores: [],
      storeData: [],
      filteredstore: [],
      categories: [
        { id: 0, name: '홈', icon: '🏠'},
        { id: 1, name: '패스트푸드', icon: '🍔'},
        { id: 2, name: '중식', icon: '🍜' },
        { id: 3, name: '분식', icon: '🌭' },
        { id: 4, name: '일식', icon: '🍣' },
        { id: 5, name: '카페·디저트', icon: '🧁' },
        { id: 6, name: '아시안', icon: '🍱' },
        { id: 7, name: '양식', icon: '🍝' },
        { id: 8, name: '피자', icon: '🍕' },
        { id: 9, name: '족발·보쌈', icon: '🥩' },
        { id: 10, name: '찜·탕', icon: '🍲'}
      ],
      selectedcategory: {name: ''}
    }
  },
  components: {
    Swiper,
    SwiperSlide
  },
  computed: {
    ...mapGetters(['getUser', 'getLikedStore', 'getCategory']),
    user() {
      return this.getUser;
    },
    category() {
      return this.getCategory;
    }
  },
  mounted() {
    this.getAllStores();
    if (this.user && this.user.id) {
      this.getStoreLike();
      this.getAllCoupons();
    }
    this.likedstore = this.getLikedStore;
    console.log('vuex 카테고리', this.category);
  },
  methods: {
    async getAllStores() {
      try {
        const response = await axios.get('http://localhost:8000/order/getallstores/');
        this.storeData = response.data;
        console.log('가게들', this.storeData);

        if (this.category) {
          this.categoryStore(this.categories.find(c => c.name === this.category));
        } else {
          this.filteredstore = this.storeData; 
          console.log('query 없을떈?', this.filteredstore);
        }

      } catch (error) {
        if (error.response) {
          console.log("API error:", error.response.data); 
        } else {
          console.log("Error occurred:", error.message);
        }
      }
    },
    categoryStore(categoryid) {
      // 카테고리 ID에 맞는 가게 데이터 필터링하기
      this.selectedcategory = categoryid;
      console.log('카테고리 아이디', categoryid);
      console.log(this.selectedcategory);
      this.$store.commit('setCategory', categoryid.name)

      if (categoryid.name === '홈') {
        this.$router.push('/');
      } else if(this.storeData && categoryid) {
        this.filteredstore = this.storeData.filter((store) => store.categories.some((category) => category === categoryid.name));
      }
    },
    async getStoreLike() {
      try {
        const response = await axios.get(`http://localhost:8000/order/getstorelikes/${this.user.id}/`);
        console.log(response.data);

        // Vuex에 likedstore 배열 저장
        this.$store.commit('setLikedStores', response.data.likes.map(like => like.store_id));
      } catch (error) {
        console.error('Error fetching liked stores:', error);
      }
    },
    detailstore(store) {
      this.$router.push('/detailstore'),
      this.$store.commit('setStore', store);
    },
    async getAllCoupons() { // 발급받은 모든 쿠폰 가져오기
      try {
        const response = await axios.get(`http://localhost:8000/order/getallcoupons/${this.user.id}/`)

        this.allcoupons = response.data.coupons;  // 응답에서 coupons 배열만 사용
        this.allcouponstores = this.allcoupons.map(coupon => coupon.store); // store만 모아서 배열에 저장
        console.log('사용자가 받은 모든 쿠폰 가져오기'
        , this.allcouponstores);  // 확인용 출력
      } catch (error) {
        console.error('Error fetching coupon:', error);
      }
    },
    goHome() {
      this.$router.push('/');
    }
  }
}
</script>