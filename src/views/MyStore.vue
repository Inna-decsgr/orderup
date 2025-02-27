<template>
  <div class="p-4">
    <div class="mb-2">
      <div>
        <div class="flex justify-between items-center">
          <p class="text-xl font-bold cursor-pointer pb-2" @click="gomystores">오더업 사장님광장</p>
        </div>
        <p class="text-[15px]">
          <span class="font-bold">{{ user.username }}</span>님
          <i class="fa-solid fa-chevron-right"></i>
        </p>
      </div>
    </div>
    <div v-if="route.path === '/mystore'" class="my-3">
      <img src="/media/Banner/selfservice.png" alt="셀프 서비스 배너">
    </div>
    <div v-if="route.path === '/mystore'" class="text-center mt-3 border-b pt-3 pb-5">
      <div>
        <button 
          v-for="menu in menus" 
          :key="menu.id" 
          class="border-1 border-gray-200 mr-3 text-3xl p-[10px] w-[100px] h-[90px] items-center rounded-3xl"
          @click="menu.click"
        >
          <span class="" v-html="menu.icon"></span>
          <p class="font-bold mt-2 text-xs">{{ menu.name }}</p>
        </button>
      </div>
    </div>
    <div v-if="route.path === '/mystore'">
      <div class="p-4 border-b font-bold text-lg">
        <p class="mb-3 cursor-pointer"><i class="fa-solid fa-list mr-3"></i>주문내역</p>
        <p class="mb-3 cursor-pointer"><i class="fa-solid fa-sack-dollar mr-3 text-yellow-500"></i>정산내역</p>
        <p class="cursor-pointer"><i class="fa-solid fa-stamp mr-3 text-red-500"></i>부가세신고내역</p>
      </div>
      <div class="p-4 border-b font-bold text-lg">
        <p class="mb-3 cursor-pointer"><i class="fa-solid fa-box mr-3 text-yellow-800"></i>상품관리</p>
        <p class="cursor-pointer"><i class="fa-solid fa-pen-to-square mr-3"></i>옵션관리</p>
      </div>
      <div class="p-4 font-bold text-lg">
        <p class="mb-3 cursor-pointer"><i class="fa-solid fa-flag mr-3 text-blue-500"></i>광고·서비스관리</p>
        <p class="cursor-pointer"><i class="fa-solid fa-calendar-days mr-3 text-green-500"></i>광고정기결제내역</p>
      </div>
    </div>
    <router-view></router-view>
  </div>
</template>


<script>
import { useRoute } from 'vue-router';

export default {
  data() {
    return {
      route: useRoute(),
      menus: [
        { id: 1, name: '전체현황', icon: '<i class="fa-solid fa-calendar text-gray-600"></i>', click: this.goallmystores },
        { id: 2, name: '가게입점', icon: '<i class="fa-solid fa-store text-violet-500"></i>', click: this.gotoRegistrationStore},
        { id: 3, name: '리뷰관리', icon: '<i class="fa-solid fa-comment text-blue-200"></i>', click: this.goallmyreviews },
        { id: 4, name: '광고관리', icon: '<i class="fa-solid fa-pencil text-blue-500"></i>' },
      ],
    }
  },
  computed: {
    user() {
      return this.$store.getters.getUser;
    },
  },
  methods: {
    gotoRegistrationStore() {
      this.$router.push('/registrationstore')
    },
    goallmystores() {
      this.$router.push('/mystore/allmystores')
    },
    goallmyreviews() {
      this.$router.push('/allmyreviews')
    },
    gomystores() {
      this.$router.push('/mystore')
    }
  }
}
</script>
