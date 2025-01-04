<template>
  <div>
    <div>
      <button class="category-btn" @click="categoryStore(categories[0])">
        <span>🍔</span>
        <p>패스트푸드</p>
      </button>
      <button class="category-btn" @click="categoryStore(categories[1])">
        <span>🍜</span>
        <p>중식</p>
      </button>
      <button class="category-btn" @click="categoryStore(categories[2])">
        <span>🌭</span><br/>
        <p class="inline-block">분식</p>
      </button>
      <button class="category-btn" @click="categoryStore(categories[3])">
        <span>🍣</span>
        <p>일식</p>
      </button>
      <button class="category-btn" @click="categoryStore(categories[4])">
        <span>🧁</span>
        <p>카페·디저트</p>
      </button>
      <button class="category-btn" @click="categoryStore(categories[5])">
        <span>🍱</span>
        <p>아시안</p>
      </button>
      <button class="category-btn" @click="categoryStore(categories[6])">
        <span>🍝</span>
        <p>양식</p>
      </button>
      <button class="category-btn" @click="categoryStore(categories[7])">
        <span>🍕</span>
        <p>피자</p>
      </button>
      <button class="category-btn" @click="categoryStore(categories[8])">
        <span>🥩</span>
        <p>족발·보쌈</p>
      </button>
      <button class="category-btn" @click="categoryStore(categories[9])">
        <span>🍲</span>
        <p>찜·탕</p>
      </button>
    </div>
    <div v-if="filteredstore && filteredstore.length">
      <div v-for="store in filteredstore" :key="store.id" >
        <h3 @click="detailstore({id:store.id, name: store.name})" style="cursor:pointer">
          {{ store.name }}
        </h3>
        <div v-if="user && user.id">
          <StoreLike :storeid="store.id" :likedstore="this.likedstore || []" />
        </div>
        <p v-if="!allcouponstores.includes(store.name)" style="font-weight: bold; color: blueviolet;">첫 주문 할인 쿠폰</p>
        <p>{{ store.address }}</p>
        <p>{{ store.phonenumber }}</p>
        <p>⭐ {{ store.rating }}</p>
        <p>{{ store.description }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import StoreLike from '../components/StoreLike.vue'
import { mapGetters } from 'vuex';
import axios from 'axios';

export default {
  data() {
    return {
      likedstore: [],
      allcouponstores: [],
      storeData: [],
      filteredstore: [],
      categories: [
        { id: 1, name: '패스트푸드' },
        { id: 2, name: '중식' },
        { id: 3, name: '분식' },
        { id: 4, name: '일식' },
        { id: 5, name: '카페·디저트' },
        { id: 6, name: '아시안' },
        { id: 7, name: '양식' },
        { id: 8, name: '피자' },
        { id: 9, name: '족발·보쌈' },
        { id: 10, name: '찜·탕'}
      ],
      category: ''
    }
  },
  components: {
    StoreLike
  },
  computed: {
    ...mapGetters(['getUser', 'getLikedStore']),
    user() {
      return this.getUser;
    },
  },
  mounted() {
    this.getAllStores();
    this.category = this.$route.query.category;
    if (this.user && this.user.id) {
      this.getStoreLike();
      this.getAllCoupons();
    }
    this.likedstore = this.getLikedStore;
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
      if (this.storeData && categoryid) {
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
  }
}
</script>