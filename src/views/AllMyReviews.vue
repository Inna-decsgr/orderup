<template>
  <div>
    <div>
      <div class="flex items-center">
        <i class="fa-solid fa-arrow-left pr-4 cursor-pointer" @click="this.$router.push('/myorderup')"></i>
        <p class="font-bold text-lg">리뷰관리</p>
      </div>
    </div>
    <div v-if="userreviews.length > 0" class="p-3">
      <p class="font-bold pb-2 border-b mb-2">내가 쓴 총 리뷰 {{userreviews.length}}개</p>
      <div v-for="review in userreviews" :key="review.id">
        <p><strong>{{ review.store.store_name }}</strong></p>
        <div class="flex text-sm items-center py-2">
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
          <span class="text-gray-400 pl-2">{{ formatRelativeDate(review.date) }}</span>
        </div>
        <p class="text-sm font-bold">{{ review.content }}</p>
        <div v-if="review.image_url" class="py-2">
          <img :src="review.image_url" alt="가게 이미지" class="w-[200px] h-[200px] rounded-lg">
        </div>
        <button @click="gotoMyReview(review.store)" class="bg-violet-500 text-white font-bold w-full text-sm p-2 mt-3 rounded-md">후기 보러가기</button>
      </div>
    </div>
    <div v-if="count > 0" class="bg-gray-100 p-3 text-sm font-bold text-center mt-5 rounded-md">
      <p>아직 작성하지 않은 리뷰가 {{ count }}개 있습니다.</p>
      <button @click="this.$router.push('/orderlist')" class="bg-violet-500 text-white w-full p-2 mt-3">리뷰 쓰러가기</button>
    </div>
    <div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      userreviews: [],
      orderlist: [],
      filteredorders: [],
      count: 0
    }
  },
  computed: {
    user() {
      return this.$store.getters.getUser;
    },
  },
  mounted() {
    this.getAllReviews();
    this.getOrderList();
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
    },
    async getOrderList() {
      const orders = await axios.get(`http://localhost:8000/order/getorderlist/${this.user.id}`);
      this.orderlist = orders.data.sort((a, b) => new Date(b.ordered_at) - new Date(a.ordered_at));
      this.filteredorders = this.orderlist.filter(order => order.status === 'delivered' && !order.review)
      this.count = this.filteredorders.length;
      console.log('리뷰 남겨야하는 주문들', this.filteredorders);
      console.log('주문 내역들', this.orderlist);
    },
  }
}
</script>