<template>
  작성한 리뷰
  <div v-for="review in reviews" :key="review.id">
      <p><strong>{{ review.username }}</strong></p>
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
      <span>{{ formattedDate(review.date) }}</span>
      <br/>
      <img v-if="review.image_url" :src="review.image_url" alt="Review Image" class="review-image">
      <p>{{ review.content }}</p>
  </div>
</template>

<script>
import axios from 'axios';
import { formatDate } from '../utils/dateutils';

export default {
  data() {
    return {
      reviews: []
    }
  },
  computed: {
    user() {
      return this.$store.getters.getUser;
    },
    storeid() {
      return this.$route.query.storeid;
    }
  }, 
  mounted() {
    this.getMyReview();
  },
  methods: {
    async getMyReview() {
      const response = await axios.get('http://localhost:8000/order/getmyreview/', {
        params: {
          userid: this.user.id,
          storeid: this.storeid
        }
      });
      console.log(response.data);
      this.reviews = response.data.reviews
    },
    formattedDate(date) {
      return formatDate(date);
    },
  }
}
</script>