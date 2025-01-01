<template>
  <div>
    <div>
      <p><strong>찜한 가게</strong></p>
      <p>총 {{ this.userlikedstores.length }}개</p>
      <div v-for="store in this.userlikedstores" :key="store.id" @click="gotoStoreDetail(store)" class="store_item">
        <div class="store_image">
          <img :src="store.image_url" alt="가게 이미지" style="width: 250px; height: 200px;">
        </div>
        <div class="store_info">
          <p><strong>{{ store.store_name}}</strong></p>
          <p>⭐ {{ store.rating }} ({{ store.review_count }})</p>
          <p class="store_description">{{ store.description }}</p>
          <p>배달팁 {{ store.delivery_fee }}원</p>
        </div>
      </div>
    </div>
    <div>
      <p><strong>찜 많은 가게를 추천해요</strong></p>
      <div v-for="store in likedallstores" :key="store.id" class="liked_store_item">
        <div class="liked_store_image">
          <img :src="store.store.image_url" alt="가게 이미지">
        </div>
        <div class="liked_store_info">
          <p class="liked_store_name"><strong>{{ store.store.name }}</strong> <span>⭐ {{ store.store.rating }}</span></p>
          <p class="liked_store_address">{{ store.store.address }}</p>
          <p class="liked_store_delivery">배달팁 : {{ Number(store.store.delivery_fee).toLocaleString() }}원</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';

export default {
  data() {
    return {
      userlikedstores: [],
      likedallstores: []
    }
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

.liked_store_item {
  display: flex; 
  align-items: center; 
  margin-bottom: 20px;
  border-bottom: 1px solid #ddd; 
  padding-bottom: 10px;
}

.liked_store_image img {
  width: 100px;
  height: 100px;
  border-radius: 8px; 
  object-fit: cover;
  margin-right: 15px; 
}

.liked_store_info {
  flex: 1;
}

.liked_store_name {
  font-size: 14px;
  color: #666;
  margin-bottom: 5px;
}

.liked_store_delivery {
  font-size: 14px;
  color: #333;
}
</style>