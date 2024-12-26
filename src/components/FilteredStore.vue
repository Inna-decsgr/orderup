<template>
  <div>
    <div v-if="filteredstore && filteredstore.length">
      <div v-for="store in filteredstore" :key="store.id" >
        <h3 @click="detailstore({id:store.id, name: store.name})" style="cursor:pointer">
          {{ store.name }}
        </h3>
        <div v-if="user && user.id">
          <StoreLike :storeid="store.id" :likedstore="this.likedstore || []" />
        </div>
        <p v-if="!allcouponstores.includes(store.name)" style="font-weight: bold; color: blueviolet;">첫 주문 할인 쿠폰</p>
        <p>{{ store.address }}</p>
        <p>{{ store.phonenumber }}</p>
        <p>{{ store.rating }}</p>
        <p>{{ store.description }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import StoreLike from '../components/StoreLike.vue'
import { mapGetters } from 'vuex';
import axios from 'axios';

export default {
  data() {
    return {
      likedstore: [],
      allcouponstores: []
    }
  },
  components: {
    StoreLike
  },
  props: {
    filteredstore: {
      type: Array,
      required: true
    }
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
  },
  methods: {
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