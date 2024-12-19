<template>
  <div>
    <div v-if="filteredstore && filteredstore.length">
      <div v-for="store in filteredstore" :key="store.id" >
        <h3 @click="detailstore({id:store.id, name: store.name})" style="cursor:pointer">
          {{ store.name }}
        </h3>
        <StoreLike :storeid="store.id" :likedstore="this.likedstore || []" />
        <p v-if="!couponstores.includes(store.id)" style="font-weight: bold; color: blueviolet;">첫 주문 할인 쿠폰</p>
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
      couponstores: []
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
    ...mapGetters(['getUser']),
    user() {
      return this.getUser;
    },
  },
  mounted() {
    this.getStoreLike();
    this.getOrderStore();
  },
  methods: {
    async getStoreLike() {
      const response = await axios.get(`http://localhost:8000/order/getstorelikes/${this.user.id}/`, { storeid: this.storeid });
      console.log(response.data);
      this.likedstore = response.data.likes.map(like => like.store_id);
    },
    async getOrderStore() {
      console.log(this.user.id)
      const response = await axios.get(`http://localhost:8000/order/getorderlist/${this.user.id}`);
      console.log('요청 데이터', response.data);
      this.couponstores = response.data.map(order => order.restaurant.id)
      console.log('주문한 가게들g', this.couponstores);
    },
    detailstore(store) {
      this.$router.push('/detailstore'),
      this.$store.commit('setStore', store);
    }
  }
}
</script>