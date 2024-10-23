<template>
  <div>
    <p>로그인 페이지</p>
    <p>로그인</p>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="logininput" class="form-label">아이디</label>
        <input 
          type="email" 
          class="form-control"
          v-model="loginid"
          id="logininput" 
          placeholder="email@email.com"
          required
        >
      </div>
      <div>
        <label for="passwordinput" class="col-form-label">비밀번호</label><span class="formtext">
          8-20자 이내여야 합니다.
        </span>
        <input 
          type="password" 
          id="passwordinput" 
          class="form-control"
          v-model="loginpassword"
          aria-describedby="passwordHelpInline" 
          placeholder="비밀번호"
          required
        >
      </div>
      <button type="submit">로그인</button>
      <p>아직 계정이 없으신가요?</p>
      <button @click.prevent="gotoSignUp">회원가입</button>
      <p v-if="errorMessage">{{ errorMessage }}</p>
    </form>
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

        // CSRF 토큰을 Vuex에 저장
        this.$store.commit('setCsrfToken', csrfToken);

        const storedCsrfToken = localStorage.getItem('csrfToken');
        if (storedCsrfToken) {
          axios.defaults.headers.common['X-CSRFToken'] = storedCsrfToken;
        }

        const response = await axios.post('http://localhost:8000/order/login/', {
          loginid: this.loginid,
          loginpassword: this.loginpassword
        }, {
          headers: {
            'X-CSRFToken': csrfToken,  // 수정된 부분
          }
        });

        console.log('로그인 성공', response.data);

        // 로그인 성공 시 Vuex에 사용자 정보 저장
        const userData = response.data.user;
        await this.login(userData);

        alert(`안녕하세요. ${userData.username}님!`)
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