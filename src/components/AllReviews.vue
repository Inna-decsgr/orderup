<template>
  <div>
    <div v-if="reviews.length > 0">
      <p><strong>모든 리뷰</strong></p>
      <div v-for="review in reviews" :key="review.review_id" class="review">
        <p><strong>{{ review.user.username }}</strong></p>
        <span>{{ review.rating }}</span>
        <div class="star-rating">
          <div class="stars">
            <i
              v-for="star in 5"
              :key="star" 
              class="fa fa-star"
              :class="{'active': star <= review.rating}"
            ></i><span v-if="review.rating !== 0">{{ review.rating }}</span>
          </div>
        </div>
        <span>{{ new Date(review.date).toLocaleDateString() }}</span>
        <br/>
        <img v-if="review.image_url" :src="review.image_url" alt="Review Image" class="review-image">
        <p>{{ review.content }}</p>
      </div>
    </div>
    <p v-else>등록된 리뷰가 없습니다.</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      reviews: []
    }
  },
  computed: {
    store() {
      return this.$store.getters.getStore;
    },
  },
  created() {
    this.AllReviews();
  },
  methods: {
    isFullStar(star) {
      // 완전히 채워진 별 표시 조건
      return star <= this.rating;
    },
    async AllReviews() {
      try {
        const response = await axios.get(`http://localhost:8000/order/allreviews/${this.store.id}`);
        console.log(response.data);
        this.reviews = response.data.reviews
      } catch (error) {
        console.error('Error fetching reviews:', error);
      }
    }
  }
}
</script>






<style>
.review {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
}
.review-image {
  max-width: 300px;
  height: auto;
}

.star-rating {
  width: 150px;
  text-align: center;
  border-radius: 5px;
  padding: 5px;
}

.stars {
  display: flex;
  justify-content: center;
}

.stars .fa {
  font-size: 15px;
  color: #ccc; /* 기본 별 색상 */
  cursor: pointer;
}

.stars .fa.active{
  color: rgb(250, 215, 19);
  /*text-shadow: 0 0 5px rgb(230, 204, 62);*/
}

</style>