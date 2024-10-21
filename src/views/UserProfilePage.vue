<template>
  <div v-if="user && !isEditing">
    <h2>사용자 프로필</h2>
    <button @click="editMode">수정</button>
    <button @click="confirmDelete">탈퇴하기</button>
    <div>
      <div>
        <p>사용자 이름</p>
        <p>{{ this.user.username }}</p>
      </div>
      <div>
        <p>이메일</p>
        <p>{{ this.user.email }}</p>
      </div>
      <div>
        <p>전화번호</p>
        <p>{{ this.user.phone_number }}</p>
      </div>
      <div>
        <p>주소</p>
        <p>{{ this.user.address }}</p>
      </div>
    </div>
  </div>
  <div v-else>
    <EditProfile :user="user" :cancel="handleCancel"/>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import EditProfile from '../components/EditProfile.vue'; 
import axios from 'axios';


export default {
  components: {
    EditProfile
  },
  data() {
    return {
      isEditing: false,
    }
  },
  computed: {
    ...mapGetters(['getUser']),
    user() {
      return this.getUser;
    },
  },
  methods: {
    ...mapActions(['logout']),
    editMode() {
      this.isEditing = true;
      console.log(this.isEditing);
    },
    handleCancel() {
      this.isEditing = false;
    },
    confirmDelete() {
      const isConfirmed = confirm('정말로 회원을 탈퇴하시겠습니까?');
      if (isConfirmed) {
        this.deleteUser(); 
      }
    },
    getCsrfToken() {
      const csrfCookie = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='));
      
      if (csrfCookie) {
        return csrfCookie.split('=')[1];  // 'csrftoken=' 이후의 값을 반환
      } else {
        return null;  // CSRF 토큰을 찾지 못하면 null 반환
      }
    },
    mounted() {
      // CSRF 토큰을 초기 설정에 추가
      axios.defaults.headers.common['X-CSRFToken'] = this.getCsrfToken();
    },
    async deleteUser() {
      try {
        const csrfToken = this.getCsrfToken();

        await axios.delete(`http://localhost:8000/order/deleteuser/${this.user.id}/`, {
          headers: {
            'X-CSRFToken': csrfToken,
          }
        });

        alert('탈퇴가 성공적으로 완료되었습니다.');
        await this.logout();
        this.$router.push('/');
      } catch (error) {
        console.error('사용자 삭제 중 오류 발생', error);
      }
    }
  }
};
</script>
