<template>
  <div class="p-3">
    <div class="flex items-center">
      <button @click="gotoHome"><i class="fa-solid fa-arrow-left"></i></button>
      <div class="relative flex items-center w-[100%] max-w-[400px]">
        <i class="fa-solid fa-x absolute right-[150px] text-[8px] bg-gray-400 text-white flex items-center justify-center w-4 h-4 rounded-full cursor-pointer" @click="removekeyword"></i>
        <input 
          type="text" 
          v-model="keyword"
          @keyup.enter="filterResults"
          class="border-b ml-3 font-bold outline-none py-[8px] pr-[8px] pl-[32px]"
        >
      </div>
    </div>
    <p class="font-bold mt-3">배달</p>
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
    this.filterResults();
  },
  methods: {
    async filterResults() {
      try {
        if (!this.keyword.trim()) {
          alert('검색어를 입력하세요.');
          return;
        }
        // 가게 이름에 검색 키워드가 포함된 결과 가져오기
        const storeResponse = await axios.get("http://localhost:8000/order/getallstores/");
        const stores = storeResponse.data.filter((store) => store.name.includes(this.keyword))
        console.log('가게 이름에 포함된 결과', stores);

        // 메뉴 이름에 검색 키워드가 포함된 결과 가져오기
        const menuResponse = await axios.get(`http://localhost:8000/order/getallmenus/${this.keyword}/`);
        const restaurants = menuResponse.data.map(menu => menu.restaurant);
        // 가게 아이디를 기준으로 중복된 가게는 제외하고 필터링
        const uniqueRestaurants = restaurants.filter(
          (restaurant, index, self) =>
            index === self.findIndex(r => r.id === restaurant.id)
        );

        console.log('메뉴 이름에 포함된 결과 (중복 제거)', uniqueRestaurants);

        // 두 결과 합치기 (중복 제거)
        const combinedResults = [...stores, ...uniqueRestaurants].filter(
          (store, index, self) => 
            index === self.findIndex((s) => s.id === store.id)
        )

        console.log('최종 검색 결과', combinedResults);
        this.filteredStore = combinedResults;
      } catch (error) {
        console.error('메뉴 데이터를 가져오는 중 에러 발생:', error);
        return [];
      }
    },
    gotoHome() {
      this.$router.push('/')
    },
    removekeyword() {
      this.keyword = null
    }
  }
}
</script>