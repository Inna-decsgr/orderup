<template>
  <div>
    리뷰 관리
    내가 쓴 총 리뷰 -개
    <div>
      <div v-for="review in userreviews" :key="review.id">
        <p><strong>{{ review.store.store_name }}</strong></p>
        <button @click="gotoMyReview(review.store)">후기 보러가기</button>
        <div class="star-rating">
          <div class="stars">
            <i
              v-for="star in 5"
              :key="star" 
              class="fa fa-star"
              :class="{'active': star <= review.rating}"
            ></i><span v-if="review.rating !== 0" class="ratingscore">{{ review.rating }}</span>
          </div>
        </div>
        <p>{{review.date}}</p>
        <p>{{ review.content }}</p>
        <div v-if="review.image_url">
          <img :src="review.image_url" alt="가게 이미지" style="width: 200px; height: 200px;">
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      userreviews: []
    }
  },
  computed: {
    user() {
      return this.$store.getters.getUser;
    },
  },
  mounted() {
    this.getAllReviews();
  },
  methods: {
    async getAllReviews() {
      try {
        const response = await axios.get(`http://localhost:8000/order/getalluserreviews/${this.user.id}/`)
        this.userreviews = response.data.reviews
        console.log('사용자가 작성한 모든 리뷰', this.userreviews);
      }catch (error) {
        console.error('Error fetching reviews:', error);
      }
    },
    gotoMyReview(store) {
      this.$router.push('/myreview');
      this.$store.commit('setStore', store)
    }
  }
}
</script>