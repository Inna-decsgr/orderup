<template>
  <nav>
    <router-link to="/">Home</router-link>
    <button v-if="!isLoggedIn" @click="gotoLogin">로그인</button>
    <div v-else>
      <button @click="logout">로그아웃</button>
      <button v-if="!isUserProfilePage" @click="gotoUserProfile">사용자 페이지</button>
    </div>

  </nav>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters(['isLoggedIn']),
    isUserProfilePage() {
      return this.$route.name === 'userprofile';
    }
  },
  methods: {
    gotoLogin() {
      this.$router.push('/login');
    },
    logout() {
      this.$store.dispatch('logout');
      this.$router.push('/');
    },
    gotoUserProfile() {
      this.$router.push('/userprofile')
    },
  }
}
</script>