<template>
  최근에 주문한 가게들(캐러셀)
  <div v-for="store in this.stores" :key="store.id">
    <div class="p-4">
      <img :src="store.restaurant.image_url" alt="가게 이미지" style="width: 250px; height: 200px;">
      <p><strong>{{ store.restaurant.name }}</strong></p>
      <p>{{ store.restaurant.address }}</p>
      <p>⭐{{ store.restaurant.rating }}</p>
      <p>{{ store.restaurant.description }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      stores: []
    }
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
      console.log(response.data);
      this.stores = response.data.map(order => ({
        restaurant: order.restaurant,
        ordered_at: order.ordered_at
      }))
        .sort((a, b) => new Date(b.ordered_at) - new Date(a.ordered_at));

      console.log('주문한 가게들', this.stores);
    },
  }
}
</script>