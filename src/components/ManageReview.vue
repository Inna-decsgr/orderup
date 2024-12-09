<template>
  리뷰 관리하기
  <div v-if="reviews.length > 0">
    <AllReviews :reviews="reviews" :getallreviews="getAllReviews" />
  </div>
</template>

<script>
import axios from 'axios';
import AllReviews from '../components/AllReviews.vue'


export default {
  components: {
    AllReviews
  },
  props: {
    storeid: {
      type: String,
      required: true
    },
  },
  data() {
    return {
      reviews : []
    }
  },
  mounted() {
    this.getAllReviews();
  },
  methods: {
    async getAllReviews() {
      try {
        const response = await axios.get(`http://localhost:8000/order/allreviews/${this.storeid}/`);
        console.log(response.data);
        this.reviews = response.data.reviews;
        console.log('리뷰 개수', this.reviews .length);
      } catch (error) {
        console.error('Error fetching reviews:', error);
      }
    }
  }
}
</script>