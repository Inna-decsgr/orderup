<template>
  <nav>
    <router-link to="/">Home</router-link>
    <button v-if="!isLoggedIn" @click="gotoLogin">로그인</button>
    <div v-else>
      <button @click="logout">로그아웃</button>
      <button v-if="!isUserProfilePage" @click="gotoUserProfile">사용자 페이지</button>
      <button v-if="isOwner" @click="gotoStoreRegistration">가게 등록</button>
    </div>

  </nav>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters(['isLoggedIn', 'getUser']),
    isUserProfilePage() {
      return this.$route.name === 'userprofile';
    },
    isOwner() {
      // getUser를 사용해서 사용자 정보에서 is_owner 확인
      return this.getUser && this.getUser.is_owner;
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
    gotoStoreRegistration() {
      // 가게 등록 페이지로 이동
      this.$router.push('/storeregistration');
    }
  }
}
</script>