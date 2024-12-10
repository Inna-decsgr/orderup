<template>
  <div id="app">
    <MainNavbar v-if="!isLoginPage" />
    <div v-if="user">
      <p>{{ user.username }}님 <span v-if="user.is_owner" style="font-weight: bold;">- 사업자</span></p>
      <div v-if="!user.is_owner">
        <button @click="gotoCart"><i class="fa-solid fa-cart-shopping"></i></button>
        <button @click="gotoOrderList">주문 내역</button>
      </div>
    </div>
    <router-view/>
  </div>
</template>

<script>
import MainNavbar from './components/MainNavbar.vue'
import { mapGetters } from 'vuex';

export default {
  components: {
    MainNavbar,
  },
  watch: {
    user(newValue) {
      console.log('사용자 정보가 변경되었습니다.', newValue)
    }
  },
  computed: {
    ...mapGetters(['getUser']),
    user() {
      return this.getUser;
    },
    isLoginPage() {
      return this.$route.name === 'login' || this.$route.name === 'signup';
    }
  },
  methods: {
    gotoCart() {
      this.$router.push('/mycart')
    },
    gotoOrderList() {
      this.$router.push('/orderlist')
    }
  }
}
</script>

