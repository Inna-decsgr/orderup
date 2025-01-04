<template>
  <div class="home">
    <div class="flex justify-between items-center">
      <p v-if="user"><i class="fa fa-map-marker"></i> <strong>{{ this.user.address }}</strong></p>
      <div class="flex items-center ml-auto">
        <button type="button" class="btn btn-light text-xs" v-if="!isLoggedIn" @click="gotoLogin">로그인</button>
        <button v-if="user && user.is_owner" @click="gotoMyStore" class="mr-5">
          <i class="fa-solid fa-store"></i>
        </button>
        <button v-if="user" @click="gotoMyCart" class="mr-2">
          <i class="fa-solid fa-cart-shopping"></i>
        </button>
      </div>
    </div>
    <div>
      <SearchBar />
    </div>
    <div>
      <div>
        <button class="category-btn" @click="categoryStore(categories[0])">
          🍔
          <p>패스트푸드</p>
        </button>
        <button class="category-btn" @click="categoryStore(categories[1])">
          🍜
          <p>중식</p>
        </button>
        <button class="category-btn" @click="categoryStore(categories[2])">
          🌭
          <p>분식</p>
        </button>
        <button class="category-btn" @click="categoryStore(categories[3])">
          🍣
          <p>일식</p>
        </button>
        <button class="category-btn" @click="categoryStore(categories[4])">
          🧁
          <p>카페·디저트</p>
        </button>
        <button class="category-btn" @click="categoryStore(categories[5])">
          🍱
          <p>아시안</p>
        </button>
        <button class="category-btn" @click="categoryStore(categories[6])">
          🍝
          <p>양식</p>
        </button>
        <button class="category-btn" @click="categoryStore(categories[7])">
          🍕
          <p>피자</p>
        </button>
        <button class="category-btn" @click="categoryStore(categories[8])">
          🥩
          <p>족발·보쌈</p>
        </button>
        <button class="category-btn" @click="categoryStore(categories[9])">
          🍲
          <p>찜·탕</p>
        </button>
      </div>
      <div>
        <FilteredStore :filteredstore="filteredData"/>
      </div>
      <div v-if="user && user.id">
        <RecentOrderStore />
      </div>
      <div style="margin-top: 50px; margin-bottom: 50px;">
        <SaleBanner />
      </div>
      <div v-if="!showfilteredstore">
        <OrderChart />
      </div>
      <div>
        <BottomBanner />
      </div>
      {{ this.storeData }}
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import FilteredStore from '../components/FilteredStore.vue'
import SearchBar from '../components/SearchBar.vue'
import OrderChart from '../components/OrderChart.vue'
import RecentOrderStore from '../components/RecentOrderStore.vue'
import SaleBanner from '../components/SaleBanner.vue'
import BottomBanner from '../components/BottomBanner.vue'
import { mapGetters } from 'vuex';



export default {
  components: {
    FilteredStore,
    SearchBar,
    OrderChart,
    RecentOrderStore,
    SaleBanner,
    BottomBanner
  },
  computed: {
    ...mapGetters(['isLoggedIn', 'getUser']),
    user() {
      return this.$store.getters.getUser;
    }
  },
  data() {
    return {
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
      storeData: [],
      filteredData: [],
      showfilteredstore:false
    }
  },
  async created() {
    this.getAllStores();
  },
  methods: {
    async getAllStores() {
      try {
        const response = await axios.get('http://localhost:8000/order/getallstores/');
        this.storeData = response.data;
      } catch (error) {
        if (error.response) {
          console.log("API error:", error.response.data); // 오류 메시지 출력
        } else {
          console.log("Error occurred:", error.message);
        }
      }
    },
    categoryStore(categoryid) {
      // 카테고리 ID에 맞는 가게 데이터 필터링하기
      this.filteredData = this.storeData.filter((store) => store.categories.some((category) => category === categoryid.name));
      this.showfilteredstore = true
    },
    gotoLogin() {
      this.$router.push('/login');
    },
    gotoMyCart() {
      this.$router.push('/mycart')
    },
    gotoMyStore() {
      this.$router.push('/mystore');
    },
  }
}
</script>
