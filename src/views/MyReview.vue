<template>
  작성한 리뷰
  <button v-if="!isEditReview" @click="editReview">리뷰 수정하기</button>
  <div v-if="!isEditReview">
    <div v-for="review in reviews" :key="review.id">
      <p><strong>{{ store.name }}</strong></p>
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
  </div>
  <div v-else>
    <EditMyReview :cancel="cancelEdit" :reviews="reviews"/>
  </div>
</template>

<script>
import axios from 'axios';
import { formatDate } from '../utils/dateutils';
import EditMyReview from '../components/EditMyReview.vue';

export default {
  components: {
    EditMyReview
  },
  data() {
    return {
      reviews: [],
      isEditReview: false
    }
  },
  computed: {
    user() {
      return this.$store.getters.getUser;
    },
    store() {
      return this.$store.getters.getStore;
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
          storeid: this.store.id
        }
      });
      console.log(response.data);
      this.reviews = response.data.reviews
    },
    formattedDate(date) {
      return formatDate(date);
    },
    editReview() {
      this.isEditReview = true;
    },
    cancelEdit() {
      this.isEditReview = false;
    }
  }
}
</script>