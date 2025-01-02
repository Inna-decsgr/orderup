<template>
  <div>
    <swiper>
      <swiper-slide v-for="image in Bannerimages" :key="image.id">
        <img :src="image.ref" :alt="`세일 배너 이미지 ${image.id}`" class="banner_image"/>
        <p class="banner_index">{{ image.id + " / " + Bannerimages.length }}</p>
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

<style>
.banner_image {
  display: block;
  max-width: 100%;
  height: auto;
  margin: 0 auto;
}


.banner_index {
  position: absolute;
  bottom: 10px; /* 아래쪽에 위치 */
  right: 180px;  /* 오른쪽에 위치 */
  color: white; /* 글자 색 */
  background-color: rgba(0, 0, 0, 0.2);
  padding: 5px 15px;
  border-radius: 5px; /* 모서리 둥글게 */
}
</style>
