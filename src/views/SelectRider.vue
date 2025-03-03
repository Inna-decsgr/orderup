<template>
  <div class="bg-black opacity-85 p-3 text-white">
    <p class="font-bold text-xl">라이더가 지정되었어요</p>
    <div v-for="rider in riders" :key="rider.id" class="">
      <p class="bg-violet-500 w-[80px] text-center py-1 px-2 text-sm rounded-sm mt-2 font-bold">한집배달</p>
      <p class="font-bold pt-3">배정된 라이더 정보</p>
      <div class="flex items-center my-3">
        <p class="font-bold bg-white w-[70px] h-[70px] rounded-full flex flex-col justify-center text-center mr-3 text-black">{{ rider.name }}</p>
        <p class="font-bold">{{ rider.phone_number }}</p>
      </div>
      <div v-if="order.status === 'delivering'">
        <p>음식 배달중입니다<i class="fa-solid fa-bicycle"></i>💨</p>
      </div>
      <button @click="foodPickUp" class="bg-violet-500 w-full p-2 font-bold rounded-sm">
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
      alert('배달을 시작합니다.');
      this.$router.push("/manageStore");
      console.log(response.data);
    }
  }

}
</script>