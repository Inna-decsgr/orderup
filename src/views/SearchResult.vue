<template>
  <div>
    <div>
      <button @click="gotoHome"><i class="fa-solid fa-arrow-left"></i></button>
      <input 
        type="text" 
        v-model="keyword"
        @keyup.enter="searchstores"
        class="border ml-3 pl-2 font-bold"
      >
    </div>
    <div v-if="filteredStore">
      <SearchFiltered :filteredstore="filteredStore"/>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import SearchFiltered from '../components/SearchFiltered.vue'

export default {
  components: {
    SearchFiltered
  },
  data() {
    return {
      storeData: [],
      stores: [],
      filteredStore: [],
      keyword: this.$route.query.keyword || '',
    }
  },
  mounted() {
    this.getStoreMenus();
  },
  methods: {
    async getStoreMenus() {
      try {
        if (!this.keyword.trim()) {
          alert('검색어를 입력하세요.');
          return;
        }

        const response = await axios.get(`http://localhost:8000/order/getallmenus/${this.keyword}/`);
        const restaurants = response.data.map(menu => menu.restaurant);
        // 가게 아이디를 기준으로 중복된 가게는 제외하고 필터링
        const uniqueRestaurants = restaurants.filter(
          (restaurant, index, self) =>
            index === self.findIndex(r => r.id === restaurant.id)
        );

        console.log('중복 제거된 레스토랑', uniqueRestaurants);
        this.filteredStore = uniqueRestaurants;
      } catch (error) {
        console.error('메뉴 데이터를 가져오는 중 에러 발생:', error);
        return [];
      }
    },
    async searchstores() {
      await this.getStoreMenus();
    },
    gotoHome() {
      this.$router.push('/')
    },
    filterStores(keyword) {
      this.filteredStore = this.storeData.filter((store) => {
        return store.name && store.name.includes(keyword);
      })
    }
  }
}
</script>