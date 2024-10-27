<template>
  <div>
    <div>내 가게</div>
    <button @click="gotoRegistrationStore">새 가게 등록하기</button>
  </div>
  <div v-if="storedata">
    <ul>
      <li v-for="(store, index) in storedata" :key="index">
        <p>{{ index }}.</p>
        <p>소유주: {{ store.owner }}</p>
        <p>가게 이름: {{ store.name }}</p>
        <p>가게 전화번호: {{ store.phone_number }}</p>
        <p>가게 설명: {{ store.description }}</p>
        <img :src="store.image_url" alt="가게 이미지" style="width:300px; height:200px">
        <p>가게 주소: {{ store.address }}</p>
        <p>카테고리: {{ store.categories[0] }}</p>
        <p>가게 운영시간: {{ store.operating_hours }}</p>
        <p>가게 평점: {{ store.rating }}</p>
      </li>
    </ul>
  </div>
</template>


<script>
import axios from 'axios';
import { mapGetters } from 'vuex';

export default {
  data() {
    return {
      storedata: []
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

        console.log('내 가게 가져오기 성공', response.data);
        this.storedata = response.data;

        // 가게 가져오기 성공 시 반환받은 데이터 출력
        console.log('내 가게', response.data);
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
    }
  }
}
</script>
