<template>
  <div>
    검색 결과 페이지
    <p>'{{ keyword }}'(으)로 검색된 결과</p>
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
      filteredStore: []
    }
  },
  computed: {
    keyword() {
      return this.$route.query.keyword;
    }
  },
  mounted() {
    this.getSearchResult();
  },
  methods: {
    async getSearchResult() {
      try {
        const response = await axios.get('http://localhost:8000/order/getallstores/');
        this.storeData = response.data;

        this.filteredStore = this.storeData.filter((store) => {
          return store.name && store.name.includes(this.keyword);
        })
      } catch (error) {
        if (error.response) {
          console.log("API error:", error.response.data); // 오류 메시지 출력
        } else {
          console.log("Error occurred:", error.message);
        }
      }
    }
  }
}
</script>