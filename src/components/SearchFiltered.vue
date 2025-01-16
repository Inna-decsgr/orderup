<template>
  <div>
    <div v-if="filteredstore && filteredstore.length">
      <div v-for="store in filteredstore" :key="store.id" @click="detailstore({id:store.id, name: store.name})" class="flex items-center cursor-pointer border-b py-3">
        <img :src="store.imageurl" alt="가게 이미지" class="w-[65px] h-[65px] mr-2 rounded-md">
        <div>
          <p class="font-bold flex items-center">
            <span class="text-sm pr-2">{{ store.name }}</span>
            <span v-if="!allcouponstores.includes(store.name)" class="text-violet-500 text-xs bg-violet-100 inline-block py-[2px] px-[5px] rounded-sm">첫 주문 할인 쿠폰</span>
          </p>
          <p class="font-bold text-xs">
            <span>⭐ {{ store.rating }}</span>
            <span v-if="store.reviews.length > 0"> (+{{ store.reviews.length }})</span>
          </p>
          <p class="line-clamp-1 text-xs text-gray-500 py-[2px]">{{ store.description }}</p>
          <p class="text-xs"><span class="text-gray-500">배달팁</span> <span class="font-bold">{{ Number(store.deliveryfee).toLocaleString() }}원</span></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import axios from 'axios';

export default {
  data() {
    return {
      likedstore: [],
      allcouponstores: [],
      storeData: [],
      filteredData: this.storeData,
    }
  },
  props: {
    filteredstore: {
      type: Array,
      required: true
    },
  },
  computed: {
    ...mapGetters(['getUser', 'getLikedStore']),
    user() {
      return this.getUser;
    },
    store() {
      return this.$store.getters.getStore;
    }
  },
  mounted() {
    if (this.user && this.user.id) {
      this.getStoreLike();
      this.getAllCoupons();
    }
    this.likedstore = this.getLikedStore;
    this.getAllStores();
  },
  methods: {
    async getAllStores() {
      try {
        const response = await axios.get('http://localhost:8000/order/getallstores/');
        this.storeData = response.data;
      } catch (error) {
        if (error.response) {
          console.log("API error:", error.response.data); // 오류 메시지 출력
        } else {
          console.log("Error occurred:", error.message);
        }
      }
    },
    categoryStore(categoryid) {
      // 카테고리 ID에 맞는 가게 데이터 필터링하기
      this.filteredData = this.storeData.filter((store) => store.categories.some((category) => category === categoryid.name));
      console.log('히히', this.filteredData);
    },
    async getStoreLike() {
      try {
        const response = await axios.get(`http://localhost:8000/order/getstorelikes/${this.user.id}/`);
        console.log(response.data);

        // Vuex에 likedstore 배열 저장
        this.$store.commit('setLikedStores', response.data.likes.map(like => like.store_id));
      } catch (error) {
        console.error('Error fetching liked stores:', error);
      }
    },
    detailstore(store) {
      this.$router.push('/detailstore'),
      this.$store.commit('setStore', store);
    },
    async getAllCoupons() { // 발급받은 모든 쿠폰 가져오기
      try {
        const response = await axios.get(`http://localhost:8000/order/getallcoupons/${this.user.id}/`)

        this.allcoupons = response.data.coupons;  // 응답에서 coupons 배열만 사용
        this.allcouponstores = this.allcoupons.map(coupon => coupon.store); // store만 모아서 배열에 저장
        console.log('사용자가 받은 모든 쿠폰 가져오기'
        , this.allcouponstores);  // 확인용 출력
      } catch (error) {
        console.error('Error fetching coupon:', error);
      }
    },
  }
}
</script>