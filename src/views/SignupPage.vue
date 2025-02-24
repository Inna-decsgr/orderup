<template>
  <div class="flex flex-col items-center justify-center h-screen">
    <p class="font-bold text-3xl pb-3">Orderup</p>
    <div class="border p-5 rounded-md">
      <div>
        <p class="text-xl pb-4">딱 이것만 체크하면 가입완료!</p>
      </div>
      <form @submit.prevent="registerUser" class="w-[400px]">
        <div class="pb-3">
          <label for="nameInput" class="form-label font-bold text-sm">이름</label>
          <input 
            type="text" 
            class="form-control text-sm placeholder-gray-400"
            v-model="name"
            id="nameInput" 
            placeholder="이름을 입력해주세요." 
            required
          >
        </div>
        <div class="pb-3">
          <label for="signupinput" class="form-label font-bold text-sm">아이디</label>
          <input 
            type="email" 
            class="form-control text-sm placeholder-gray-400"
            v-model="signupid"
            id="signupinput" 
            placeholder="이메일을 입력해주세요." 
            required
          >
        </div>
        <div class="pb-3">
          <label for="passwordinput2" class="col-form-label font-bold text-sm">비밀번호</label>
          <input 
            type="password" 
            id="passwordinput2" 
            class="form-control mb-1 text-sm placeholder-gray-400" 
            v-model="signupPassword"
            aria-describedby="passwordHelpInline" 
            placeholder="비밀번호를 입력해 주세요.(8자리 이상)" 
            required
          >
          <input 
            type="password" 
            id="confirmPassword" 
            class="form-control text-sm placeholder-gray-400" 
            v-model="confirmPassword" 
            aria-describedby="passwordHelpInline" 
            placeholder="비밀번호를 한번 더 입력해주세요." 
            required
          >
          <span v-if="passwordMismatch" style="color: red">
            비밀번호가 일치하지 않습니다
          </span>
        </div>
        <div class="pb-3">
          <label for="phoneNumber" class="col-form-label font-bold text-sm">휴대전화</label>
          <input 
            type="tel" 
            id="phoneNumber" 
            class="form-control text-sm placeholder-gray-400" 
            v-model="phoneNumber" 
            placeholder="전화번호를 입력해주세요." 
            required
          >
        </div>
        <div class="pb-3">
          <label for="address" class="col-form-label font-bold text-sm">주소</label>
          <input 
            type="text" 
            id="address" 
            class="form-control text-sm placeholder-gray-400" 
            v-model="address" 
            placeholder="주소를 입력해주세요." 
            required
          >
        </div>
        <div>
          <input type="checkbox" id="is_owner" v-model="isOwner">
          <label for="is_owner" class="col-form-label text-sm pl-2 pb-3">사업자일 경우 체크</label>

          <div v-if="isOwner" class="pb-3">
            <label for="reg_number" class="col-form-label font-bold text-sm">사업자등록번호</label>
            <input 
              type="text" 
              id="reg_number" 
              class="form-control text-sm placeholder-gray-400" 
              v-model="reg_number" 
              placeholder="사업자등록번호를 입력해 주세요." 
              required
            >
          </div>
        </div>

        <button type="submit" class="w-full bg-violet-500 p-2 mt-3 mb-[50px] rounded-md font-bold text-white">버튼만 누르면 가입완료!</button>
        <div class="flex justify-between text-sm">
          <p class="border-b-[1px] pb-2 border-violet-500">이미 계정이 있으신가요?</p>
          <button @click="gotoLogin" class="border py-[6px] px-3 rounded-md bg-violet-500 text-white font-bold">로그인</button>
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