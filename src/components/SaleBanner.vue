<template>
  <div>
    <swiper>
      <swiper-slide v-for="image in Bannerimages" :key="image.id">
        <img :src="image.ref" :alt="`세일 배너 이미지 ${image.id}`" class="relative"/>
        <p class="absolute bottom-3 right-4 text-white text-xs bg-black bg-opacity-50 px-4 py-[1px] border border-gray-100 rounded-xl">{{ image.id + " / " + Bannerimages.length }}</p>
      </swiper-slide>
    </swiper>
  </div>
</template>

<script>
import { Swiper, SwiperSlide } from 'swiper/vue';
import 'swiper/css';


export default {
  data() {
    return {
      Bannerimages: [
        { id: 1, ref: '/media/Banner/Sale Banner1.png' },
        { id: 2, ref: '/media/Banner/Sale Banner2.png' },
        { id: 3, ref: '/media/Banner/Sale Banner3.png' },
        { id: 4, ref: '/media/Banner/Sale Banner4.png' },
      ],
    }
  },
  components: {
    Swiper,
    SwiperSlide,
  },
};
</script>
