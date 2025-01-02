<template>
  <div v-if="stores.length > 0">
    <p style="text-align: center; margin-top: 30px;"><strong>최근에 주문한 가게들</strong></p>
    <swiper slides-per-view="3" :space-between="10">
      <swiper-slide v-for="store in stores" :key="store.id" class="recent_store_item">
        <div class="p-4" @click="gotoStoreDetail(store)">
          <div class="recent_store_content">
            <div class="recent_store_image">
              <img :src="store.restaurant.image_url" alt="가게 이미지">
            </div>
            <div class="recent_store_info">
              <p><strong>{{ store.restaurant.name }}</strong></p>
              <p v-if="store.count > 1">{{ store.count }}번 이상 주문했어요😊</p>
              <p>{{ store.restaurant.address }}</p>
              <p>⭐{{ store.restaurant.rating }}</p>
              <p class="store_description">{{ store.restaurant.description }}</p>
            </div>
          </div>
        </div>
      </swiper-slide>
    </swiper>
  </div>
</template>

<script>
import axios from 'axios';
import { Swiper, SwiperSlide } from 'swiper/vue';
import 'swiper/css';


export default {
  data() {
    return {
      stores: []
    }
  },
  components: {
    Swiper,
    SwiperSlide,
  },
  computed: {
    user() {
      return this.$store.getters.getUser;
    },
  },
  mounted() {
    this.getOrderStore()
  },
  methods: {
    async getOrderStore() {
      console.log(this.user.id)
      const response = await axios.get(`http://localhost:8000/order/getorderlist/${this.user.id}`);

      const orders = Array.isArray(response.data) ? response.data : response.data.orders;

      const storeMap = new Map();

      orders.forEach(order => {
        const restaurantId = order.restaurant.id;
        if (!storeMap.has(restaurantId)) {
          storeMap.set(restaurantId, {
            restaurant: order.restaurant,
            ordered_at: order.ordered_at,
            count: 1,
          });
        } else {
          const storeData = storeMap.get(restaurantId);
          storeData.count += 1;
          storeMap.set(restaurantId, storeData);
        }
      });

      this.stores = Array.from(storeMap.values()).sort(
        (a, b) => new Date(b.ordered_at) - new Date(a.ordered_at)
      );
      console.log('주문한 가게들', this.stores);
    },
    gotoStoreDetail(store) {
      this.$router.push('/detailstore');
      this.$store.commit('setStore', store);
      console.log(store.restaurant.id);
    }
  }
}
</script>

<style>
.recent_store_item {
  display: flex;
  align-items: center;
}

.recent_store_content {
  display: flex;
  align-items: center;
}

.recent_store_image {
  flex-shrink: 0; /* 이미지가 줄어들지 않게 설정 */
  margin-right: 15px; 
}

.recent_store_image img {
  width: 250px; /* 이미지 크기 */
  height: 200px;
  object-fit: cover; /* 이미지 비율 유지 */
}

.recent_store_info {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.recent_store_description {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: normal;
}
</style>