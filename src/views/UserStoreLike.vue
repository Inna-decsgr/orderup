<template>
  <div class="p-3 px-3">
    <p class="font-bold text-xl">찜</p>
    <p class="font-bold text-sm my-2">배달·포장</p>
    <div>
      <p class="font-bold pt-2 text-sm">총 {{ this.userlikedstores.length }}개</p>
      <div v-for="store in this.userlikedstores" :key="store.id" @click="gotoStoreDetail(store)" class="border-b flex justify-center items-center p-2 py-3">
        <div class="basis-1/5 relative">
          <img :src="store.image_url" alt="가게 이미지" class="border w-[150px] h-[100px] rounded-lg object-cover">
          <div v-if="!isoperatinghours(store.operatinghours).isOperating" class="absolute top-0 left-0 w-full h-full rounded-lg object-cover bg-black opacity-80 flex justify-center items-center">
            <span class="text-white">준비중</span>
          </div>
        </div>
        <div class="basis-4/5 p-2 px-3">
          <p class="text-[15px] font-bold">{{ store.store_name}}</p> 
          <div class="text-[14px]">
            <p class="font-bold">
              ⭐ {{ store.rating }} 
              <span v-if="store.review_count > 1" >({{ store.review_count }}+)</span>
            </p>
            <span class="line-clamp-1 ellipsis-h text-sm pb-[3px] text-[13px]">{{ store.description }}</span>
          </div>
          <p class="text-sm">
            <span class="text-gray-600">배달팁</span> 
            <span class="font-bold pl-2">{{ store.delivery_fee.toLocaleString() }}원</span>
          </p>
        </div>
      </div>
    </div>
    <div class="pt-3 pb-1">
      <p class="font-bold mb-[10px] text-sm">찜 많은 가게 추천해요</p>
      <swiper :space-between="20">
        <swiper-slide v-for="store in likedallstores" :key="store.id" class="flex items-center justify-start border rounded-[10px] p-[7px]">
          <div class="basis-1/5">
            <img :src="store.store.image_url" alt="가게 이미지" class="w-[80px] h-[80px] border rounded-[32px]">
          </div>
          <div>
            <p class="mb-[5px] font-bold">{{ store.store.name }} 
              <span class="text-sm">⭐ {{ store.store.rating }}</span>
            </p>
            <p class="text-sm">{{ store.store.address }}</p>
            <div class="flex">
              <p class="text-[14px]"><span class="text-gray-500">배달팁 : </span> {{ Number(store.store.delivery_fee).toLocaleString() }}원</p>
              <p class="text-[14px] ml-3 font-semibold">찜 갯수 : +{{ store.store.like_count }}</p>
            </div>
          </div>
        </swiper-slide>
      </swiper>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';
import { Swiper, SwiperSlide } from 'swiper/vue';
import 'swiper/css';
import { isOperatingHour } from '../utils/isoperatinghours.js';


export default {
  data() {
    return {
      userlikedstores: [],
      likedallstores: []
    }
  },
  components: {
    Swiper,
    SwiperSlide,
  },
  computed: {
    ...mapGetters(['getUser']),
    user() {
      return this.getUser;
    },
  },
  mounted() {
    this.getStoreLike();
    this.getAllLikedStore();
  },
  methods: {
    async getStoreLike() {
      // 사용자가 찜한 가게들 가져오기
      const response = await axios.get(`http://localhost:8000/order/getstorelikes/${this.user.id}/`);
      console.log(response.data);
      this.userlikedstores = response.data.likes;
      console.log('사용자가 찜한 가게들', this.userlikedstores);
    },
    gotoStoreDetail(store) {
      this.$router.push('/detailstore');
      this.$store.commit('setStore', store);
      console.log(store);
    },
    async getAllLikedStore() {
      // 찜된 모든 가게들 가져오기
      const response = await axios.get(`http://localhost:8000/order/getlikedallstores/`);
      console.log('찜된 모든 가게들', response.data.liked_stores);
      this.likedallstores = response.data.liked_stores
    },
    isoperatinghours(hour) {
      return isOperatingHour(hour);
    },
  }
}
</script>

