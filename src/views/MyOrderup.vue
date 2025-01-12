<template>
  <div class="p-3">
    <p class="font-bold">마이오더업</p>
    <div>
      <div class="flex items-center py-3">
        <div>
          <img src="/media/Profile/userprofile.png" alt="사용자 프로필 이미지" />
        </div>
        <div>
          <p @click="editmode" class="font-bold cursor-pointer">
            {{ this.user.username }}
            <span class="text-gray-400"><i class="fa-solid fa-chevron-right"></i></span>
          </p>
          <button @click="showAllReviews" class="text-sm font-bold">
            <i class="fa-regular fa-comment"></i>
            리뷰관리
          </button>
        </div>
      </div>
      <div class="pb-3">
        <img src="/media/Banner/Sale Banner4.png" alt="배너 이미지" class="rounded-lg w-full h-[160px]"/>
      </div>
    </div>
    <div>
    </div>
    <div class="border rounded-lg text-center p-3">
      <div @click="showCoupon" class="cursor-pointer">
        <img src="/media/Coupon/sale coupon.png" alt="세일 쿠폰 이미지" class="w-[100px] h-[50px] mx-auto"/>
        <p class="font-bold pt-2 text-lg">{{ allcoupons.length }}장</p>
        <button class="font-bold">쿠폰함</button>
      </div>
      <div v-if="showallcoupons">
        <p>보유쿠폰</p>
        <div v-for="coupon in allcoupons" :key="coupon.created_at">
          <div style="border: 1px solid black; margin-top: 10px;">
            <p>{{ coupon.store }} - {{ coupon.discount_amount }}원</p>
            <p>첫 주문 {{ coupon.discount_amount }}원 할인</p>
            <p>최소주문금액: 10,000원</p>
            <p>사용기간: {{ formattedDate(coupon.expired_date) }}</p>
            <button @click="goStoreDetailPage({id:coupon.store_id, name:coupon.store})">주문하러 가기</button>
          </div>
        </div>
      </div>

      <!--리뷰 리스트-->
      <div v-if="showReviews">
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
  </div>
</template>

<script>
import axios from 'axios';
import { formatDate } from '../utils/dateutils';

export default {
  data() {
    return {
      allcoupons: [],
      showallcoupons: false,
      showReviews: false,
      userreviews: []
    }
  },
  computed: {
    user() {
      return this.$store.getters.getUser;
    },
  },
  mounted() {
    this.getAllCoupons();
    this.getAllReviews();
  }, 
  methods: {
    formattedDate(date) {
      return formatDate(date);
    },
    async getAllCoupons() { // 발급받은 모든 쿠폰 가져오기
      try {
        const response = await axios.get(`http://localhost:8000/order/getallcoupons/${this.user.id}/`)
        console.log('해당 가게에서 발급받은 모든 쿠폰 가져오기', response.data);

        this.allcoupons = response.data.coupons;  // 응답에서 coupons 배열만 사용
        console.log(this.allcoupons);  // 확인용 출력
      } catch (error) {
        console.error('Error fetching coupon:', error);
      }
    },
    async getAllReviews() {
      try {
        const response = await axios.get(`http://localhost:8000/order/getalluserreviews/${this.user.id}/`)
        this.userreviews = response.data.reviews
        console.log('사용자가 작성한 모든 리뷰', this.userreviews);
      }catch (error) {
        console.error('Error fetching reviews:', error);
      }
    },
    goStoreDetailPage(store) {
      this.$router.push('/detailstore'),
      this.$store.commit('setStore', store);
    },
    showCoupon() {
      this.showallcoupons = true;
      this.showReviews = false;
    },
    showAllReviews() {
      this.showReviews = true
      this.showallcoupons = false;
    },
    gotoMyReview(store) {
      this.$router.push('/myreview');
      this.$store.commit('setStore', store)
    },
    editmode() {
      this.$router.push('/myorderup/editprofile');
    }
  }
}
</script>