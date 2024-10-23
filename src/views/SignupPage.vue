<template>
  <div>
    <p>회원가입 페이지</p>
    <p>회원가입</p>
    <form @submit.prevent="registerUser">
      <div>
        <label for="nameInput" class="form-label">이름</label>
        <input 
          type="text" 
          class="form-control"
          v-model="name"
          id="nameInput" 
          placeholder="이름을 입력해주세요" 
          required
        >
      </div>
      <div>
        <label for="signupinput" class="form-label">아이디</label>
        <input 
          type="email" 
          class="form-control"
          v-model="signupid"
          id="signupinput" 
          placeholder="email@email.com" 
          required
        >
      </div>
      <div>
        <label for="passwordinput2" class="col-form-label">비밀번호</label>
        <input 
          type="password" 
          id="passwordinput2" 
          class="form-control" 
          v-model="signupPassword"
          aria-describedby="passwordHelpInline" 
          placeholder="비밀번호" 
          required
        >
      </div>
      <div>
        <label for="confirmPassword" class="col-form-label">비밀번호 확인</label>
        <input 
          type="password" 
          id="confirmPassword" 
          class="form-control" 
          v-model="confirmPassword" 
          aria-describedby="passwordHelpInline" 
          placeholder="비밀번호를 한 번 더 입력해주세요" 
          required
        >
        <span v-if="passwordMismatch" style="color: red">
          비밀번호가 일치하지 않습니다
        </span>
      </div>
      <div>
        <label for="phoneNumber" class="col-form-label">휴대전화</label>
        <input 
          type="tel" 
          id="phoneNumber" 
          class="form-control" 
          v-model="phoneNumber" 
          placeholder="휴대전화" 
          required
        >
      </div>
      <div>
        <label for="address" class="col-form-label">주소</label>
        <input 
          type="text" 
          id="address" 
          class="form-control" 
          v-model="address" 
          placeholder="주소를 입력해주세요" 
          required
        >
      </div>
      <div>
        <input type="checkbox" id="is_owner" v-model="isOwner">
        <label for="is_owner" class="col-form-label"><span style="font-weight: bold;">사업자</span>일 경우 체크</label>

        <div v-if="isOwner">
          <label for="reg_number" class="col-form-label">사업자등록번호</label>
          <input 
            type="text" 
            id="reg_number" 
            class="form-control" 
            v-model="reg_number" 
            placeholder="사업자등록번호를 입력하세요" 
            required
          >
        </div>
      </div>

      <button type="submit">회원가입</button>
      <p>이미 계정이 있으신가요?</p>
      <button @click="gotoLogin">로그인</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      name: '',           
      signupid: '',
      signupPassword: '',
      confirmPassword: '',
      phoneNumber: '',    
      address: '',        
      errorMessage: '',
      registeredUser: '',
      isOwner: false,
      reg_number: ''
    }
  },
  computed: {
    passwordMismatch() {
      return this.signupPassword !== this.confirmPassword;
    }
  },
  methods: {
    async registerUser() {
      if (!this.passwordMismatch) {
        try {
          const csrfResponse = await axios.get("http://localhost:8000/order/csrftoken/");
          const csrfToken = csrfResponse.data.csrfToken;
        
          const response = await axios.post('http://localhost:8000/order/signup/', {
            name: this.name,            
            signupid: this.signupid,
            signuppassword: this.signupPassword,
            phoneNumber: this.phoneNumber,  
            address: this.address,
            isOwner: this.isOwner,
            regnumber: this.reg_number         
          }, {
              headers: {
              'X-CSRFToken': csrfToken,
            }
          });
          console.log('회원가입 성공', response.data);
          this.registeredUser = this.name; // 회원가입한 사용자 이름 설정

          alert(`환영합니다 ${this.name}님!`);
          this.$router.push('/login');
        } catch (error) {
          if (error.response && error.response.data) {
            this.errorMessage = error.response.data.error || '회원가입에 실패했습니다. 다시 시도해주세요.';
          } else {
            this.errorMessage = '네트워크 오류가 발생했습니다.';
          }
          console.error('회원가입 실패', error);
        }
      }
    },
    gotoLogin() {
      this.$router.push('/login')
    }
  }
}
</script>