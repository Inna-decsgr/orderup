<template>
  <div v-if="user && !isEditing">
    <div class="p-3">
      <div style="display: flex; justify-content: space-between; align-items: center;" class="px-100">
        <button @click="goBack">
          <i class="fa-solid fa-arrow-left"></i>
        </button>
        <p class="font-bold text-lg">내 정보 수정</p>
        <button class="text-sm bg-gray-50 py-1 px-2 rounded-md font-bold hover:bg-gray-50" @click="editMode">수정</button>
      </div>
      <div class="card mt-4 text-sm">
        <ul class="list-group list-group-flush">
          <li class="list-group-item">
            <div class="flex">
              <p class="font-bold block w-[110px]">이름</p>
              <p class=" text-gray-600">{{ this.user.username }}</p>
            </div>
          </li>
          <li class="list-group-item">
            <div class="flex">
              <p class="font-bold block w-[110px]">대표 이메일</p>
              <p class="text-gray-600">{{ this.user.email }}</p>
            </div>
          </li>
          <li class="list-group-item">
            <div class="flex">
              <p class="font-bold block w-[110px]">휴대폰 번호</p>
              <p class="text-gray-600">{{ this.user.phone_number }}</p>
            </div>
          </li>
          <li class="list-group-item">
            <div class="flex">
              <p class="font-bold block w-[110px]">주소</p>
              <p class="text-gray-600">{{ this.user.address }}</p>
            </div>
          </li>
          <li v-if="user.is_owner" class="list-group-item">
            <div class="flex">
              <p class="font-bold block  w-[110px]">사업자등록번호</p>
              <p class="text-gray-600">{{ this.user.business_registration_number }}</p>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
  <div v-else>
    <EditProfile :user="user" :cancel="handleCancel"/>
  </div>
  <div class="text-center pt-3">
    <button type="button" class="text-sm font-bold pr-3" style="color: rgb(143, 139, 139);" @click="logout">로그아웃</button> | 
    <button type="button" class="text-sm font-bold pl-3" @click="confirmDelete" style="color: rgb(143, 139, 139);">회원탈퇴</button>
  </div>
    
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


