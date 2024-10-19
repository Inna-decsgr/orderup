<template>
  <div id="app">
    <MainNavbar v-if="!isLoginPage" />
    <div v-if="user">
      <p>{{ user.username }}님</p>
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
  }
}
</script>

