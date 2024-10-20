<template>
  <div v-if="user && !isEditing">
    <h2>사용자 프로필</h2>
    <button @click="editMode">수정</button>
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
import EditProfile from '../components/EditProfile.vue'; 


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
    editMode() {
      this.isEditing = true;
      console.log(this.isEditing);
    },
    handleCancel() {
      this.isEditing = false;
    }
  }
};
</script>
