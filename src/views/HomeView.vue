<template>
  <div class="home">
    <span v-if="user"><i class="fa fa-map-marker"></i>{{ this.user.address }}</span>
    <div>
      <SearchBar />
    </div>
    <div>
      <button class="category-btn" @click="categoryStore(categories[0])">Fast Food</button>
      <button class="category-btn" @click="categoryStore(categories[1])">Chinese</button>
      <button class="category-btn" @click="categoryStore(categories[2])">Snack Food</button>
      <button class="category-btn" @click="categoryStore(categories[3])">Japanese</button>
      <button class="category-btn" @click="categoryStore(categories[4])">Dessert</button>
      <button class="category-btn" @click="categoryStore(categories[5])">Asian</button>
      <button class="category-btn" @click="categoryStore(categories[6])">Western Food</button>
    </div>
    <div>
      <FilteredStore :filteredstore="filteredData"/>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import FilteredStore from '../components/FilteredStore.vue'
import SearchBar from '../components/SearchBar.vue'


export default {
  components: {
    FilteredStore,
    SearchBar
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
    }
  }
}
</script>
