<template>
  <div id="app" class="p-3">
    <MainNavbar v-if="!isLoginPage" />
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
}
</script>

