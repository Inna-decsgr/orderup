<template>
  <div>
    <div class="flex items-center px-4 pt-4 bg-white">
      <p class="text-lg font-bold">내가 남긴 리뷰</p>
    </div>
    <div v-if="!isEditReview" class="p-4">
      <div v-for="review in reviews" :key="review.id">
        <div class="flex items-center">
          <div>
            <button @click="detailstore({id:store.id ||store.store_id, name: store.name || store.store_name})">
              <p class="font-bold">{{ store.name || store.store_name}}<i class="fa-solid fa-chevron-right pl-1"></i></p>
            </button>
            <div class="flex items-center gap-3 text-sm my-1">
              <div class="star-rating">
                <div class="stars">
                  <i
                    v-for="star in 5"
                    :key="star" 
                    class="fa fa-star"
                    :class="{'active': star <= review.rating}"
                  ></i>
                </div>
              </div>
              <span class="text-gray-400">{{ formatRelativeDate(review.date) }}</span>
            </div>
          </div>
          <div class="absolute right-[70px]">
            <button v-if="!isEditReview" @click="editReview" class="font-bold bg-gray-100 hover:bg-gray-200 py-1 px-2 text-xs rounded-xl mr-1">수정</button>
            <button class="font-bold bg-gray-100 hover:bg-gray-200 py-1 px-2 text-xs rounded-xl">삭제</button>
          </div>
        </div>
        <img v-if="review.image_url" :src="review.image_url" alt="Review Image" class="w-[300px] h-auto object-cover py-2">
        <div class="w-[400px]">
          <p class="text-sm">{{ review.content }}</p>
        </div>
        <div class="flex flex-wrap gap-2 pt-3">
          <p v-for="menu in review.items" :key="menu.id" class="text-sm border inline-block py-1 px-2 rounded-2xl font-bold">
            {{ menu.menu_name }}
          </p>
        </div>
      </div>
    </div>
    <div v-else>
      <EditMyReview :cancel="cancelEdit" :reviews="reviews"/>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
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
          storeid: this.store.id || this.store.store_id
        }
      });
      console.log(response.data);
      this.reviews = response.data.reviews
    },
    editReview() {
      this.isEditReview = true;
    },
    cancelEdit() {
      this.isEditReview = false;
    },
    detailstore(store) {
      this.$router.push('/detailstore'),
      this.$store.commit('setStore', store);
    },
    formatRelativeDate(dateString) {
      if (!dateString) return "날짜 없음"; // 예외 처리

      const date = new Date(dateString); // 주어진 날짜
      const today = new Date(); // 현재 날짜

      // 날짜 부분만 비교하기 위해 연, 월, 일을 추출
      const dateYear = date.getFullYear();
      const dateMonth = date.getMonth();
      const dateDay = date.getDate();

      const todayYear = today.getFullYear();
      const todayMonth = today.getMonth();
      const todayDay = today.getDate();

      // 오늘이면 "오늘"
      if (dateYear === todayYear && dateMonth === todayMonth && dateDay === todayDay) {
        return "오늘";
      }

      // 어제이면 "어제"
      today.setDate(todayDay - 1); // 어제 날짜 계산
      if (dateYear === today.getFullYear() && dateMonth === today.getMonth() && dateDay === today.getDate()) {
        return "어제";
      }

      // 그 외에는 YYYY-MM-DD 형식으로 표시
      return `${dateYear}/${String(dateMonth + 1).padStart(2, "0")}/${String(dateDay).padStart(2, "0")}`;
    }
  }
}
</script>