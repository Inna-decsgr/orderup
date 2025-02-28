<template>
  <div class="p-3">
    <div>
      <div class="flex items-center pb-3">
        <div>
          <img src="/media/Profile/userprofile.png" alt="사용자 프로필 이미지" />
        </div>
        <div>
          <p @click="profileEditmode" class="font-bold cursor-pointer">
            {{ this.user.username }}
            <span class="text-gray-400"><i class="fa-solid fa-chevron-right"></i></span>
          </p>
          <button @click="gotoAllMyReviews" class="text-sm font-bold">
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
    <div class="border rounded-lg text-center py-4 mx-auto flex justify-between">
      <div @click="gotoMyCoupons" class="cursor-pointer px-5 w-[33.33%]">
        <img src="/media/Coupon/sale coupon.png" alt="세일 쿠폰 이미지" class="w-[80px] h-[40px] mx-auto"/>
        <p class="font-bold pt-2">{{ allcoupons.length }}장</p>
        <button class="text-sm">쿠폰함</button>
      </div>
      <div class="border-x px-5 w-[33.33%]">
        <img src="/media/Coupon/point.png" alt="세일 쿠폰 이미지" class="w-[40px] h-[40px] mx-auto"/>
        <p class="font-bold pt-2">0원</p>
        <button class="text-sm">포인트</button>
      </div>
      <div class="px-5 w-[33.33%]">
        <img src="/media/Coupon/present.png" alt="세일 쿠폰 이미지" class="w-[50px] h-[40px] mx-auto"/>
        <p class="font-bold pt-2">0원</p>
        <button class="text-sm">받은 선물</button>
      </div>
    </div>

    <div class="p-3">
      <div class="pb-4">
        <p class="font-bold text-gray-400 pb-2 text-sm">혜택 정보</p>
        <div class="font-bold text-sm">
          <span class="mr-20">오더업포인트 모으기</span>
          <span>진행 중인 이벤트</span>
        </div>
      </div>
      <div class="pb-4">
        <p class="font-bold text-gray-400 pb-2 text-sm">모아보기</p>
        <p class="font-bold text-sm">서비스 전체보기</p>
      </div>
      <div>
        <p class="font-bold text-gray-400 pb-2 text-sm">문의 및 알림</p>
        <div class="font-bold text-sm">
          <div class="pb-3">
            <span class="mr-20">고객 센터</span>
            <span>자주 묻는 질문</span> <br/>
          </div>
          <div>
            <span class="mr-20">공지 사항</span>
            <span>약관 및 정책</span>
          </div>
        </div>
        <p class="text-gray-400 font-bold pt-5 text-sm text-center">Copyright OrderUp Company in Korea, All Rights Reserved.</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

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
    gotoAllMyReviews() {
      this.$router.push('/allmyreviews')
    },
    gotoMyCoupons() {
      this.$router.push('/allmycoupons')
    },
    profileEditmode() {
      this.$router.push('/myorderup/editprofile');
    }
  }
}
</script>


<style>
::-webkit-scrollbar {
  display: none;
}
</style>