<template>
  마이 오더업 페이지
  <div>
    <p>쿠폰함</p>
    <p>보유쿠폰 {{ allcoupons.length }}장</p>
  </div>
  <div v-for="coupon in allcoupons" :key="coupon.created_at">
    <div style="border: 1px solid black; margin-top: 10px;">
      <p>{{ coupon.store }} - {{ coupon.discount_amount }}원</p>
      <p>첫 주문 {{ coupon.discount_amount }}원 할인</p>
      <p>최소주문금액: 10,000원</p>
      <p>사용기간: {{ formattedDate(coupon.expired_date) }}</p>
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
    this.getAllCoupons()
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
  }
}
</script>