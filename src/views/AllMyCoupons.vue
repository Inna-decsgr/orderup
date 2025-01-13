<template>
  <div class="p-3">
    <p class="font-bold text-lg text-center">쿠폰함</p>
    <div class="my-3">
      <img src="/media/Banner/coupon banner.png" alt="쿠폰할인팩 배너" class="rounded-xl w-full h-[150px]"/>
    </div>
    <div>
      <p>보유쿠폰 {{ allcoupons.length }}장</p>
      <div v-for="coupon in allcoupons" :key="coupon.created_at">
        <div style="border: 1px solid black; margin-top: 10px;">
          <p>{{ Number(coupon.discount_amount).toLocaleString() }}원</p>
          <p>{{ coupon.store }} 신규고객쿠폰</p>
          <p>첫 주문 시 사용 가능</p>
          <p>사용기간: {{ formattedDate(coupon.expired_date) }}</p>
          <button @click="goStoreDetailPage({id:coupon.store_id, name:coupon.store})">가게 바로가기</button>
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
      allcoupons: []
    }
  },
  computed: {
    user() {
      return this.$store.getters.getUser;
    },
  },
  mounted() {
    this.getAllCoupons();
  },
  methods: {
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
    formattedDate(date) {
      const formatted = formatDate(date);
      return formatted.split(' ')[0] + ' ' + formatted.split(' ')[1] + ' ' + formatted.split(' ')[2];
    },
    goStoreDetailPage(store) {
      this.$router.push('/detailstore'),
      this.$store.commit('setStore', store);
    },
  }
}
</script>