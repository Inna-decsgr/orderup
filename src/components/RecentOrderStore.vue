<template>
  <div v-if="stores.length > 0" class="px-3">
    <p class="font-bold mb-3">최근에 주문한 가게들</p>
    <swiper slides-per-view="auto" :space-between="10">
      <swiper-slide v-for="store in stores" :key="store.id" class="flex w-[200px] h-[240px]">
        <div @click="gotoStoreDetail(store)" class="w-full object-cover">
          <div>
            <div>
              <img :src="store.restaurant.image_url" alt="가게 이미지" class="w-full h-[160px] border rounded-md">
            </div>
            <div class="p-2 text-xs">
              <p class="font-bold pb-1">
                <span class="font-bold">{{ store.restaurant.name }}</span>
                <span> ⭐{{ store.restaurant.rating }}</span>
              </p>
              <p v-if="store.count > 1" class="font-bold my-[2px]">{{ store.count }}번 이상 주문했어요😊</p>
              <p>배달팁 {{ store.restaurant.deliveryfee.toLocaleString() }}원</p>
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
