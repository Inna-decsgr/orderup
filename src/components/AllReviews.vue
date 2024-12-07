<template>
  <div>
    <div v-if="reviews.length > 0">
      <p><strong>모든 리뷰</strong></p>
      <button @click="handleCancel">X</button>
      <div v-for="review in reviews" :key="review.review_id" class="review">
        <p><strong>{{ review.user.username }}</strong></p>
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
        <span>{{ new Date(review.date).toLocaleDateString() }}</span>
        <br/>
        <img v-if="review.image_url" :src="review.image_url" alt="Review Image" class="review-image">
        <p>{{ review.content }}</p>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  props: {
    cancel: {
      type: Function,
      required: true
    },
    reviews: {
      type: Array,
      required: true
    }
  },
  computed: {
    store() {
      return this.$store.getters.getStore;
    },
  },
  methods: {
    isFullStar(star) {
      // 완전히 채워진 별 표시 조건
      return star <= this.rating;
    },
    handleCancel() {
      this.cancel();
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
  align-items: center;
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

.ratingscore {
  padding-left: 10px;
}

</style>