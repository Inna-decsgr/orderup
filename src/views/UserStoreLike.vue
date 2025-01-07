<template>
  <div class="p-3 px-3">
    <p class="font-bold text-xl">찜</p>
    <div class="bg-red-100">
      <p class="font-bold">총 {{ this.userlikedstores.length }}개</p>
      <div v-for="store in this.userlikedstores" :key="store.id" @click="gotoStoreDetail(store)" >
        <div>
          <img :src="store.image_url" alt="가게 이미지" style="width: 250px; height: 200px;">
        </div>
        <div>
          <p><strong>{{ store.store_name}}</strong></p>
          <p>⭐ {{ store.rating }} ({{ store.review_count }})</p>
          <p>{{ store.description }}</p>
          <p>배달팁 {{ store.delivery_fee }}원</p>
        </div>
      </div>
    </div>
    <div>
      <p class="font-bold mb-[10px]">찜 많은 가게 추천해요</p>
      <swiper :space-between="20">
        <swiper-slide v-for="store in likedallstores" :key="store.id" class="flex items-center justify-start border rounded-[10px] p-[7px]">
          <div class="basis-1/5">
            <img :src="store.store.image_url" alt="가게 이미지" class="w-[80px] h-[80px] border rounded-[32px]">
          </div>
          <div>
            <p class="text-[17px] mb-[5px] font-bold"><strong>{{ store.store.name }}</strong> <span>⭐ {{ store.store.rating }}</span></p>
            <p class="text-sm">{{ store.store.address }}</p>
            <div class="flex">
              <p class="text-[14px]"><span class="text-gray-500">배달팁 : </span> {{ Number(store.store.delivery_fee).toLocaleString() }}원</p>
              <p class="text-[14px]"><span class="text-gray-500 pl-3">찜 갯수 : </span>+{{ store.store.like_count }}</p>
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
    }
  }
}
</script>

<style>
.store_item {
  display: flex;
  align-items: flex-start; /* 이미지와 텍스트 상단 정렬 */
  border: 1px solid #ddd; /* 테두리 추가 */
  border-radius: 8px; /* 모서리 둥글게 */
  margin: 10px 0; /* 아이템 간격 */
  padding: 10px;
  background-color: #f9f9f9; /* 배경색 */
  transition: box-shadow 0.3s ease;
  cursor: pointer;
}

.store_item:hover {
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2); /* 호버 시 그림자 */
}

/* 이미지 영역 */
.store_image img {
  width: 150px;
  height: 150px;
  object-fit: cover; 
  border-radius: 8px;
  margin-right: 20px; /* 이미지와 텍스트 간 간격 */
}


.store_info {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.store_info p {
  margin: 5px 0; 
}

.store_info strong {
  font-size: 18px; 
  color: #333;
}

.store_info p:nth-child(2) {
  color: #ff9800;
  font-weight: bold;
}

.store_info p:last-child {
  color: #777; 
}

.store_description {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: normal;
}


</style>