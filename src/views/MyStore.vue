<template>
  <div class="p-3">
    <div class="flex justify-between items-center mb-2">
      <p class="text-xl font-bold cursor-pointer" @click="gomystores">오더업 <i class="fa-solid fa-store"></i> 사장님광장</p>
    </div>
    <div v-if="route.path === '/mystore'" class="mt-5">
      <div class="text-center py-4 border rounded-md">
        <p class="font-bold text-center pb-3 text-sm">전체 메뉴</p>
        <div>
          <button 
            v-for="menu in menus.slice(0, 4)" 
            :key="menu.id" 
            class="w-[80px] h-[90px]"
            @click="menu.click"
          >
            <span class="bg-[rgb(240,239,239)] text-3xl p-[10px] w-[70px] h-[70px] inline-flex justify-center items-center rounded-3xl" v-html="menu.icon"></span>
            <p class="font-bold mt-[3px] text-xs">{{ menu.name }}</p>
          </button>
        </div>
        <div class="mt-[15px]">
          <button
            v-for="menu in menus.slice(4, 8)"
            :key="menu.id"
            class="w-[80px] h-[90px]"
          >
            <span class="bg-[rgb(240,239,239)] text-3xl p-[10px] w-[70px] h-[70px] inline-flex justify-center items-center rounded-3xl" v-html="menu.icon"></span>
            <p class="font-bold mt-[3px] text-xs">{{ menu.name }}</p>
          </button>
        </div>
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
        { id: 1, name: '전체현황', icon: '<i class="fa-solid fa-calendar"></i>', click: this.goallmystores },
        { id: 2, name: '가게등록', icon: '<i class="fa-solid fa-store"></i>', click: this.gotoRegistrationStore},
        { id: 3, name: '리뷰관리', icon: '<i class="fa-solid fa-comment"></i>', click: this.goallmyreviews },
        { id: 4, name: '공지·한마디', icon: '<i class="fa-solid fa-pencil"></i>' },
        { id: 5, name: '메뉴관리', icon: '<i class="fa-solid fa-rectangle-list"></i>' },
        { id: 6, name: '메뉴품질', icon: '<i class="fa-solid fa-trash"></i>' },
        { id: 7, name: '광고관리', icon: '<i class="fa-solid fa-flag"></i>' },
        { id: 8, name: '광고정기결제', icon: '<i class="fa-solid fa-circle-check"></i>' },
      ],
    }
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
