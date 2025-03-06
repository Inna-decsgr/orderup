<template>
  <nav>
    <div class="flex items-center justify-center text-center gap-10 font-bold fixed bottom-0 left-0 right-0 bg-white p-4 shadow-lg text-xs z-10">
      <router-link to="/">
        <i class="fa-solid fa-house"></i><br/>
        홈
      </router-link>
      <router-link to="/mycart">
        <i class="fa-solid fa-cart-shopping"></i><br/>
        장바구니
        <span v-if="cart.length > 0" class="bg-violet-500 text-xs text-white py-[2px] px-[6px] rounded-full">{{ cart.length }}</span>
      </router-link>
      <router-link to="/userlike">
        <i class="fa-solid fa-heart"></i><br/>
        찜
      </router-link>
      <router-link to="/orderlist">
        <i class="fa-solid fa-clipboard-list"></i><br/>
        주문 내역
      </router-link>
      <router-link to="/myorderup">
        <i class="fa-solid fa-face-smile"></i><br/>
        마이오더업
      </router-link>
    </div>
  </nav>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters(['getUser']),
    isOwner() {
      // getUser를 사용해서 사용자 정보에서 is_owner 확인
      return this.getUser && this.getUser.is_owner;
    },
    cart() {
      return this.$store.getters.getMenuCart;
    }
  },
}
</script>