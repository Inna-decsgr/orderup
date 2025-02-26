<template>
  <div>
    <div class="py-3">
      <p class="font-bold pb-3">내 가게</p>
      <ul v-if="storedata">
        <li v-for="(store, index) in storedata" :key="index" class="border p-3 rounded-md mb-4">
          <div class="text-sm">
            <div class="flex justify-between items-center mb-2">
              <p><span class="font-bold">{{ index+1 }}번째 가게</span></p>
              <button @click="gotoManageStore({store, index})" class="bg-violet-500 text-white py-1 px-2 rounded-md text-sm">가게 관리</button>
            </div>
            <span class="font-bold">* 상호 대표 이미지</span>
            <div class="my-2">
              <img :src="imageSrc(store.image_url)" alt="가게 이미지" class="w-[200px] h-[150px] rounded-md">
            </div>
            <p><span class="font-bold">소유주</span> {{ store.owner }}</p>
            <p><span class="font-bold">상호명</span> {{ store.name }}</p>
            <p><span class="font-bold">전화번호</span> {{ store.phone_number }}</p>
            <p class="font-bold">대표 설명</p>
            <p>{{ store.description }}</p>
            <p><span class="font-bold">주소</span> {{ store.address }}</p>
            <p><span class="font-bold">분류</span> {{ store.categories[0] }}</p>
            <p><span class="font-bold">운영시간</span> {{ store.operating_hours }}</p>
            <p><span class="font-bold">평점</span> {{ store.rating }}</p>
            <p><span class="font-bold">배달료</span> {{ store.delivery_fee }}원</p>
          </div>
        </li>
      </ul>
    </div>
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
  mounted() {
    this.getMyStore();
  },
  methods: {
    async getMyStore() {
      try {
        // CSRF 토큰 요청
        const csrfResponse = await axios.get("http://localhost:8000/order/csrftoken/");
        const csrfToken = csrfResponse.data.csrfToken;

        const response = await axios.get(`http://localhost:8000/order/mystoreinfo/${this.userid}`, {
          headers: {
            'X-CSRFToken': csrfToken,  
          }
        });

        this.storedata = response.data;
        console.log('가게들', this.storedata);
      } catch (error) {
        if (error.response && error.response.status === 400) {
          this.errorMessage = error.response.data.message || '내 가게 정보를 불러오는 데 실패했습니다.';
        } else {
          this.errorMessage = '서버와의 통신에 문제가 발생했습니다.';
        }
        console.error('내 가게 가져오기 실패', error);
      }
    },
    gotoManageStore({ store }) {
      this.$router.push('/manageStore');
      this.$store.commit('setStore', store);
    },
    imageSrc(imageurl) {
      try {
        // URL 디코딩 (한글 파일명 깨짐 방지)
        imageurl = decodeURIComponent(imageurl);
      } catch (e) {
        console.error("URL 디코딩 실패:", e);
      }
      // 공백을 `_`로 변환 (Django에서 저장된 파일명과 맞추기)
      imageurl = imageurl.replace(/ /g, "_");
      // `http://` 또는 `https://`로 시작하면 그대로 사용
      if (imageurl.startsWith("http://") || imageurl.startsWith("https://")) {
        // 만약 "http://localhost:8000/media/"로 시작하면 "/images/" 추가
        if (imageurl.startsWith("http://localhost:8000/media/")) {
          return imageurl.replace("/media/", "/media/images/");
        }
        return imageurl; // 기존 URL 유지
      }
      // 상대 경로라면 `http://localhost:8000`을 붙여서 반환
      return `http://localhost:8000${imageurl}`;
    }
  }
}
</script>