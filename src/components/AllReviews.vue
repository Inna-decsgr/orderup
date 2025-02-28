<template>
  <div>
    <div v-if="reviews.length > 0">
      <p class="my-3"><strong>리뷰목록 (총{{ reviews.length }}개)</strong></p>
      <button v-if="user && !user.is_owner" @click="handleCancel">X</button>
      <div v-for="review in reviews" :key="review.review_id" class="relative review">
        <div class="flex items-center">
          <div class="star-rating mr-2">
            <div class="stars">
              <i
                v-for="star in 5"
                :key="star" 
                class="fa fa-star"
                :class="{'active': star <= review.rating}"
              ></i>
            </div>
          </div>
          <div class="flex items-center text-sm font-bold text-gray-400">
            <span class="mr-1">{{ new Date(review.date).toLocaleDateString() }}</span>
            <i class="fa-solid fa-circle text-[5px] mr-1"></i>
            <p>{{ review.user.username }}</p>
          </div>
        </div>
        <div class="my-2">
          <ul class="flex">
            <li v-for="menu in review.menus" :key="menu.menu_id">
              <span class="bg-gray-200 py-1 px-2 rounded-md mr-2 font-bold text-sm">{{ menu.name }}</span>
            </li>
          </ul>
        </div>
        <p class="text-gray-400 text-sm mt-5">작성된 리뷰</p>
        <p class="font-bold text-sm mb-4">{{ review.content }}</p>
        <img v-if="review.image_url" :src="review.image_url" alt="리뷰 이미지" class="w-[150px] h-[150px] object-cover rounded-md">
        <div class="absolute bottom-[-50px] right-0">
          <button v-if="user && user.is_owner" @click="removeReview(review.review_id)" class="font-bold text-red-500 text-center mt-4 border-1 border-red-500 rounded-[4px] py-2 px-3 hover:bg-red-100">삭제</button>
        </div>
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

  margin-bottom: 10px;
}
.star-rating {
  text-align: center;
  border-radius: 5px;
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