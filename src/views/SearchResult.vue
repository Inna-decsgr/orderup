<template>
  <div>
    검색 결과 페이지
    <p>'{{ keyword }}'(으)로 검색된 결과</p>
    <div v-if="filteredStore">
      <FilteredStore :filteredstore="filteredStore"/>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import FilteredStore from '../components/FilteredStore.vue'

export default {
  components: {
    FilteredStore
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
        console.log('검색 결과', response.data);
        this.storeData = response.data;

        // 키워드 전체 문자열을 포함하는 가게들만 저장
        this.filteredStore = this.storeData.filter((store) => store.name.includes(this.keyword));
        console.log(this.filteredStore);
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