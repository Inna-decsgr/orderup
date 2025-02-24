<template>
  <div class="flex flex-col items-center justify-center h-screen">
    <div class="border py-[60px] px-[40px] rounded-md">
      <div class="relative flex justify-between items-center w-[350px]">
        <button @click="gotohome" class="absolute text-2xl">
          <i class="fa-solid fa-arrow-left"></i>
        </button>
        <p class="absolute font-bold text-3xl right-[30%]">Orderup</p>
      </div>
      <form @submit.prevent="handleLogin">
        <div class="mt-[50px]">
          <input 
            type="email" 
            class="border rounded-md w-[350px] outline-none p-2 mb-2 text-sm"
            v-model="loginid"
            placeholder="이메일을 입력해주세요"
            required
          >
        </div>
        <div class="mb-4">
          <input 
            type="password"
            class="border rounded-md w-[350px] outline-none p-2 text-sm"
            v-model="loginpassword"
            placeholder="비밀번호를 입력해주세요"
            required
          >
        </div>
        <button type="submit" class="w-full bg-violet-500 p-2 rounded-md mb-[50px] font-bold text-white">로그인</button>
        <div class="text-center text-sm flex justify-between items-center">
          <p class="border-b-[1px] pb-2 border-violet-500">아직 계정이 없으신가요?</p>
          <button @click.prevent="gotoSignUp" class="border py-[6px] px-3 rounded-md bg-violet-500 text-white font-bold">회원가입</button>
        </div>
      </form>
    </div>
    <div class="text-xs text-gray-500 py-[70px] text-center">
      <p>이용약관 | 개인정보처리방침 | 책임의 한계와 법적고지 | 회원정보 고객센터 </p>
      <p><span class="text-lg font-bold">Orderup</span> <span class="text-xs text-gray-500">Copyright Orderup Corp. All Rights Reserved.</span></p>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import axios from 'axios';

export default {
  data() {
    return {
      loginid: '',
      loginpassword: '', 
      errorMessage: ''
    }
  },
  methods: {
    ...mapActions(['login']),
    async handleLogin() {
      try {
        // CSRF 토큰 요청
        const csrfResponse = await axios.get("http://localhost:8000/order/csrftoken/");
        const csrfToken = csrfResponse.data.csrfToken;

        const response = await axios.post('http://localhost:8000/order/login/', {
          loginid: this.loginid,
          loginpassword: this.loginpassword
        }, {
          headers: {
            'X-CSRFToken': csrfToken,  // 수정된 부분
          }
        })
        console.log('로그인 성공', response.data.user.username);

        // 로그인 성공 시 Vuex에 사용자 정보 저장
        const userData = response.data.user;
        await this.login(userData);
        this.$router.push('/');
      } catch (error) {
        if (error.response && error.response.status === 400) {
          this.errorMessage = error.response.data.message || '로그인에 실패했습니다. 아이디와 비밀번호를 확인하세요.';
        } else {
          this.errorMessage = '서버와의 통신에 문제가 발생했습니다.';
        }
        console.error('로그인 실패', error);
      }
    },
    gotoSignUp() {
      this.$router.push('/signup');
    },
    gotohome() {
      this.$router.push('/')
    }
  }
}
</script>

<style>
.formtext {
  font-size: 10px;
  color: gray;
  margin-left: 10px;
}
</style>