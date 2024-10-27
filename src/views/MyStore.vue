<template>
  <div>
    <div>내 가게</div>
    <button @click="gotoRegistrationStore">새 가게 등록하기</button>
  </div>
  <div>
    <ul v-if="storedata">
      <li v-for="(store, index) in storedata" :key="index">
        <div v-if="EditNumber === index">
          <EditStore :store="store" :cancel="handleCancel" />
        </div>
        <div v-else>
          <p>{{ index }}.</p>
          <button @click="editMode(index)">수정</button>
          <p>소유주: {{ store.owner }}</p>
          <p>가게 이름: {{ store.name }}</p>
          <p>가게 전화번호: {{ store.phone_number }}</p>
          <p>가게 설명: {{ store.description }}</p>
          <img :src="store.image_url" alt="가게 이미지" style="width:300px; height:200px">
          <p>가게 주소: {{ store.address }}</p>
          <p>카테고리: {{ store.categories[0] }}</p>
          <p>가게 운영시간: {{ store.operating_hours }}</p>
          <p>가게 평점: {{ store.rating }}</p>
          </div>
      </li>
    </ul>
  </div>
</template>


<script>
import axios from 'axios';
import { mapGetters } from 'vuex';
import EditStore from '../components/EditStore.vue'

export default {
  components: {
    EditStore
  },
  data() {
    return {
      storedata: [],
      EditNumber: null,
    }
  },
  computed: {
    ...mapGetters(['getUserId']),
    userid() {
      return this.getUserId;
    },
  },
  async mounted() {
    this.getMyStore();
  },
  methods: {
    async getMyStore() {
      try {
        // CSRF 토큰 요청
        console.log(this.userid);
        const csrfResponse = await axios.get("http://localhost:8000/order/csrftoken/");
        const csrfToken = csrfResponse.data.csrfToken;

        const response = await axios.get(`http://localhost:8000/order/mystoreinfo/${this.userid}`, {
          headers: {
            'X-CSRFToken': csrfToken,  
          }
        });

        this.storedata = response.data;
      } catch (error) {
        if (error.response && error.response.status === 400) {
          this.errorMessage = error.response.data.message || '내 가게 정보를 불러오는 데 실패했습니다.';
        } else {
          this.errorMessage = '서버와의 통신에 문제가 발생했습니다.';
        }
        console.error('내 가게 가져오기 실패', error);
      }
    },
    gotoRegistrationStore() {
      this.$router.push('/registrationstore')
    },
    editMode(index) {
      this.EditNumber = index;
    },
    handleCancel() {
      this.EditNumber = null;
    }
  }
}
</script>
