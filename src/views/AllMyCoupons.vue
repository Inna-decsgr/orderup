<template>
  <div class="p-3">
    <p class="font-bold text-lg text-center">쿠폰함</p>
    <div class="my-3">
      <img src="/media/Banner/coupon banner.png" alt="쿠폰할인팩 배너" class="rounded-xl w-full h-[150px]"/>
    </div>
    <div>
      <p class="font-bold mt-4">보유쿠폰 {{ allcoupons.length }}장</p>
      <div v-for="coupon in allcoupons" :key="coupon.created_at">
        <div class="border my-3 rounded-xl shadow-md">
          <div class="py-3 px-4">
            <p class="text-3xl font-bold text-orange-400">{{ Number(coupon.discount_amount).toLocaleString() }}원</p>
            <div class="flex text-xs pt-1">
              <p class="mr-2 bg-[#41bfda] p-1 rounded-md text-white">가게배달</p>
              <p class="bg-[#b47614] p-1 rounded-md text-white">첫주문</p>
            </div>
            <p class="font-bold pt-3">{{ coupon.store }} 신규고객쿠폰</p>
            <p class="text-gray-400 text-xs pt-[4px] pb-[2px]">첫 주문 시 사용 가능</p>
            <p class="text-gray-400 text-xs">사용기간: {{ formattedDate(coupon.expired_date) }}</p>
          </div>
          <div class="py-[13px] text-center border-t">
            <button @click="goStoreDetailPage({id:coupon.store_id, name:coupon.store})" class="font-semibold">가게 바로가기</button>
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