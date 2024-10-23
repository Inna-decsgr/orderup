<template>
  <div>
    <h2>프로필 수정</h2>
    <div v-if="user">
      <form @submit.prevent="updateUser" class="form-label">
        <label for="username">사용자 이름</label>
        <input 
          type="text" 
          id="username" 
          v-model="form.username"
          class="form-control"
          required 
        />
        <label for="email" class="form-label">이메일</label>
        <input 
          type="email" 
          id="email" 
          v-model="form.email" 
          class="form-control"
          required 
        />
        <label for="phonenumber" class="form-label">전화번호</label>
        <input 
          type="tel" 
          id="tel" 
          v-model="form.phone_number" 
          class="form-control"
          required 
        />
        <label for="address" class="form-label">주소</label>
        <input 
          type="text" 
          id="address" 
          v-model="form.address" 
          class="form-control"
          required 
        />
        <label for="is_owner" class="form-label" v-if="form.is_owner">사업자로 등록됨</label>

        <div v-if="form.is_owner">
          <label for="business_registration_number" class="form-label">사업자 등록 번호</label>
          <input 
            type="text" 
            id="business_registration_number" 
            v-model="form.business_registration_number" 
            class="form-control"
          />
        </div>
        <button type="submit">저장</button>
        <button @click="handleCancel">취소</button>
      </form>
    </div>
    <div v-else>
      <p>사용자 정보를 불러오는 중입니다...</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    user: {
      type: Object,
      required: true
    },
    cancel: {
      type: Function,
      required: true
    }
  },
  data() {
    return {
      form: { ...this.user }, // 사용자 정보를 기반으로 초기화
      originalUser: { ...this.user },
    };
  },
  methods: {
    async updateUser() {
      const updatedUser = {
        username: this.form.username,
        email: this.form.email,
        phone_number: this.form.phone_number,
        address: this.form.address,
        is_owner: this.form.is_owner, 
        business_registration_number: this.form.business_registration_number  
      };

      try {
        const csrfResponse = await axios.get("http://localhost:8000/order/csrftoken/");
        const csrfToken = csrfResponse.data.csrfToken;
        await axios.put(`http://localhost:8000/order/edituser/${this.user.id}/`, updatedUser, {
          headers: {
            'X-CSRFToken': csrfToken,
          }
        });

        // 사용자 정보가 수정된 후, 새로운 정보를 다시 받아옴
        const response = await axios.get(`http://localhost:8000/order/getuser/${this.user.id}/`);

        // Vuex 스토어에 새로운 사용자 정보 업데이트
        this.$store.commit('setUser', response.data);

        console.log('사용자 정보가 업데이트되었습니다:', response.data);
        alert('사용자 정보 수정이 완료되었습니다.');

        // 수정 모드 해제해서 수정 컴포넌트 감추기
        this.cancel();
      } catch (error) {
        console.error('사용자 정보 업데이트 중 오류 발생:', error);
      }
    },
    handleCancel() {
      this.cancel(); // 부모에게 취소 이벤트 전달
      this.form = { ...this.originalUser }; // 원래 사용자 정보로 폼 초기화
    }
  },
  watch: {
    user: {
      immediate: true,
      handler(newValue) {
        this.form = { ...newValue };  // 사용자가 변경되면 폼도 업데이트
        this.originalUser = { ...newValue }; // 원래 사용자 정보 업데이트
      }
    }
  }
};
</script>
