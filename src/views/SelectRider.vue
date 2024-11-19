<template>
  <div>
    <h5><strong>배달 지정된 라이더</strong></h5>
    <div v-for="rider in riders" :key="rider.id">
      <p>{{ rider.name }}</p>
      <p>{{ rider.phone_number }}</p>
      <div v-if="order.status === 'delivering'">
        <p>음식 배달중입니다<i class="fa-solid fa-bicycle"></i>💨</p>
      </div>
      <button @click="foodPickUp">
        {{ order.status === 'delivering' ? '배달완료' : '배달 픽업 완료' }}
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      riders: [],
    }
  },
  computed: {
    order() {
      return JSON.parse(this.$route.query.order);
    },
  }, 
  mounted() {
    this.getRiderInfo();
  },
  methods: {
    async getRiderInfo() {
      try {
        const response = await axios.get('http://localhost:8000/order/riderinfo/');
        console.log(response.data);
        this.riders = response.data.rider_info
      } catch (error) {
        console.error('Error fetching rider info:', error);
      }
    },
    async foodPickUp() {
      const csrfResponse = await axios.get("http://localhost:8000/order/csrftoken/");
      const csrfToken = csrfResponse.data.csrfToken;
      const response = await axios.put(`http://localhost:8000/order/pickupfood/${this.order.order_id}/`, null, {
        headers: {
            'X-CSRFToken': csrfToken,
          }
      });
      console.log(response.data);
    }
  }

}
</script>