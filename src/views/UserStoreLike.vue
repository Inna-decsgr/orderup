<template>
  <div>
    <p><strong>찜</strong></p>
    <p>총 {{ this.likedstores.length }}개</p>
    <div v-for="store in this.likedstores" :key="store.id" @click="gotoStoreDetail(store)" class="store_item">
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
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';

export default {
  data() {
    return {
      likedstores : []
    }
  },
  computed: {
    ...mapGetters(['getUser']),
    user() {
      return this.getUser;
    },
  },
  mounted() {
    this.getStoreLike()
  },
  methods: {
    async getStoreLike() {
      const response = await axios.get(`http://localhost:8000/order/getstorelikes/${this.user.id}/`, { storeid: this.storeid });
      console.log(response.data);
      this.likedstores = response.data.likes;
      console.log('사용자가 찜한 가게들', this.likedstores);
    },
    gotoStoreDetail(store) {
      this.$router.push('/detailstore');
      this.$store.commit('setStore', store);
      console.log(store);
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