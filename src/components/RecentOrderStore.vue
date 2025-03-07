<template>
  <div v-if="stores.length > 0" class="px-3">
    <p class="font-bold mb-3">최근에 주문한 가게들</p>
    <swiper slides-per-view="auto" :space-between="10">
      <swiper-slide v-for="store in stores" :key="store.id" class="flex w-[200px] h-[240px]">
        <div @click="gotoStoreDetail(store)" class="w-full object-cover">
          <div>
            <div>
              <img :src="imageSrc(store.restaurant.image_url)" alt="가게 이미지" class="w-full h-[160px] border rounded-md">
            </div>
            <div class="p-2 text-xs">
              <p class="font-bold pb-[1px]">
                <span class="font-bold">{{ store.restaurant.name }}</span>
                <span> ⭐{{ store.restaurant.rating }}</span>
              </p>
              <p class="pb-[5px]">배달팁 {{ store.restaurant.deliveryfee.toLocaleString() }}원</p>
              <p v-if="store.count > 1" class="font-bold">{{ store.count }}번 이상 주문했어요😊</p>
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
      this.$store.commit('setStore', store.restaurant);
      console.log(store.restaurant.id);
    },
    imageSrc(imageurl) {
      try {
        // URL 디코딩 (한글 파일명 깨짐 방지)
        imageurl = decodeURIComponent(imageurl);
      } catch (e) {
        console.error("URL 디코딩 실패:", e);
      }
      // 공백을 `_`로 변환 (Django에서 저장된 파일명과 맞추기)
      imageurl = imageurl.replace(/ /g, "_");
      // `http://` 또는 `https://`로 시작하면 그대로 사용
      if (imageurl.startsWith("http://") || imageurl.startsWith("https://")) {
        // 만약 "http://localhost:8000/media/"로 시작하면 "/images/" 추가
        if (imageurl.startsWith("http://localhost:8000/media/images")) {
          return imageurl; // 기존 URL 유지
        }
        if (imageurl.startsWith("http://localhost:8000/media/")) {
          return imageurl.replace("/media/", "/media/images/");
        }
        return imageurl
      }
      // 상대 경로라면 `http://localhost:8000`을 붙여서 반환
      return `http://localhost:8000${imageurl}`;
    },
  }
}
</script>
