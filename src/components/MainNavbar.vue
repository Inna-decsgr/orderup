<template>
  <nav>
    <router-link to="/">Home</router-link>
    <button v-if="!isLoggedIn" @click="gotoLogin">로그인</button>
    <div v-else>
      <button v-if="isOwner" @click="gotoMyStore">내 가게</button>
    </div>

  </nav>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters(['isLoggedIn', 'getUser']),
    isOwner() {
      // getUser를 사용해서 사용자 정보에서 is_owner 확인
      return this.getUser && this.getUser.is_owner;
    }
  },
  methods: {
    gotoLogin() {
      this.$router.push('/login');
    },
    gotoMyStore() {
      this.$router.push('/mystore');
    }
  }
}
</script>