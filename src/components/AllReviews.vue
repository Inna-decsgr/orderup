<template>
  <div>
    <div v-if="reviews.length > 0">
      <p><strong>모든 리뷰</strong></p>
      <button v-if="user && !user.is_owner" @click="handleCancel">X</button>
      <div v-for="review in reviews" :key="review.review_id" class="review">
        <button v-if="user && user.is_owner" @click="removeReview(review.review_id)">삭제하기</button>
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
import axios from 'axios';

export default {
  props: {
    cancel: {
      type: Function,
      required: false
    },
    reviews: {
      type: Array,
      required: true
    },
    getallreviews: {
      type: Function,
      required: false
    }
  },
  computed: {
    store() {
      return this.$store.getters.getStore;
    },
    user() {
      return this.$store.getters.getUser;
    }
  },
  methods: {
    isFullStar(star) {
      // 완전히 채워진 별 표시 조건
      return star <= this.rating;
    },
    handleCancel() {
      this.cancel();
    },
    async removeReview(reviewid) {
      const isConfirmed = window.confirm('리뷰를 삭제하시겠습니까?');

      if(isConfirmed) {
        const csrfResponse = await axios.get("http://localhost:8000/order/csrftoken/");
        const csrfToken = csrfResponse.data.csrfToken;

        const response = await axios.delete(`http://localhost:8000/order/removereview/${reviewid}/`, {
          headers: {
            'X-CSRFToken': csrfToken,
          }
        });
        console.log(response.data);
        alert("리뷰가 성공적으로 삭제되었습니다.");
        this.getallreviews();
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