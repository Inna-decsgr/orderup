<template>
  <div v-if="user && !isEditing">
    <div>
      <div style="display: flex; justify-content: space-between; align-items: center;" class="px-100">
        <button @click="goBack">
          <i class="fa-solid fa-arrow-left"></i>
        </button>
        <h5><strong>내 정보 수정</strong></h5>
        <button class="btn btn-light" @click="editMode">수정</button>
      </div>
      <div class="card" style="width: 25rem; margin-top: 20px; margin-bottom: 20px;">
        <ul class="list-group list-group-flush">
          <li class="list-group-item"><p><strong>이름</strong> {{ this.user.username }}</p></li>
          <li class="list-group-item"><p><strong>대표 이메일</strong> {{ this.user.email }}</p></li>
          <li class="list-group-item"><p><strong>휴대폰 번호</strong> {{ this.user.phone_number }}</p></li>
          <li class="list-group-item"><p><strong>주소</strong> {{ this.user.address }}</p></li>
          <li v-if="user.is_owner" class="list-group-item"><p><strong>사업자등록번호</strong> {{ this.user.business_registration_number }}</p></li>
        </ul>
      </div>
    </div>
  </div>
  <div v-else>
    <EditProfile :user="user" :cancel="handleCancel"/>
  </div>
  <button type="button" class="btn" style="color: rgb(143, 139, 139);" @click="logout">로그아웃</button> | 
  <button type="button" class="btn" @click="confirmDelete" style="color: rgb(143, 139, 139);">회원탈퇴</button>
    
</template>

<script>
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import EditProfile from './EditProfile.vue'; 
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
    ...mapGetters(['getUser', 'isLoggedIn']),
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
    async deleteUser() {
      try {
        const csrfResponse = await axios.get("http://localhost:8000/order/csrftoken/");
        const csrfToken = csrfResponse.data.csrfToken;
        
        await axios.delete(`http://localhost:8000/order/deleteuser/${this.user.id}/`, {
          headers: {
            'X-CSRFToken': csrfToken,
          }
        });

        alert('탈퇴가 성공적으로 완료되었습니다.');
        this.logout();
        this.$router.push('/');
      } catch (error) {
        console.error('사용자 삭제 중 오류 발생', error);
      }
    },
    goBack() {
      this.$router.push('/myorderup')
    },
    logout() {
      this.$store.dispatch('logout');
      this.$router.push('/'); 
    },
  }
};
</script>


