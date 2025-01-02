<template>
  <div class="home">
    <span v-if="user"><i class="fa fa-map-marker"></i>{{ this.user.address }}</span>
    <div>
      <SearchBar />
    </div>
    <div v-if="!user || (user && !user.is_owner)">
      <div>
        <button class="category-btn" @click="categoryStore(categories[0])">
          <i class="fa-solid fa-burger"></i>
          <p>Fast Food</p>
        </button>
        <button class="category-btn" @click="categoryStore(categories[1])">
          <i class="fa-solid fa-bowl-food"></i>
          <p>Chinese</p>
        </button>
        <button class="category-btn" @click="categoryStore(categories[2])">
          <i class="fa-solid fa-hotdog"></i>
          <p>Snack Food</p>
        </button>
        <button class="category-btn" @click="categoryStore(categories[3])">
          <i class="fa-solid fa-fish"></i>
          <p>Japanese</p>
        </button>
        <button class="category-btn" @click="categoryStore(categories[4])">
          <i class="fa-solid fa-ice-cream"></i>
          <p>Dessert</p>
        </button>
        <button class="category-btn" @click="categoryStore(categories[5])">
          <i class="fa-solid fa-bowl-rice"></i>
          <p>Asian</p>
        </button>
        <button class="category-btn" @click="categoryStore(categories[6])">
          <i class="fa-solid fa-shrimp"></i>
          <p>Western Food</p>
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
    user() {
      return this.$store.getters.getUser;
    }
  },
  data() {
    return {
      categories: [
        { id: "1", name: "Fast Food" },
        { id: "2", name: "Chinese" },
        { id: "3", name: "Snack Food" },
        { id: "4", name: "Japanese" },
        { id: "5", name: "Dessert" },
        { id: "6", name: "Asian" },
        { id: "7", name: "Western Food" },
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
    }
  }
}
</script>
