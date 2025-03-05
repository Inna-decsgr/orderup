<template>
  <div>
    <div class="w-[430px] mx-auto">
      <ul v-if="storedata" class="space-y-12">
        <li v-for="(store, index) in storedata" :key="index" class="relactive border rounded-md pb-[110px]">
          <div class="text-sm">
            <div class="relative items-center mb-10">
              <img :src="imageSrc(store.image_url)" alt="가게 이미지" class="w-full h-auto aspect-[4/3] object-cover rounded-md">
              <div class="absolute top-[90%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[400px] h-[320px] rounded-md bg-white text-center shadow-lg p-4">
                <p class="font-bold text-[20px]">{{ store.name }}</p>
                <p class="font-bold text-xs pt-1">{{ generatecode(index)}} - {{ store.categories[0] }}</p>
                <div class="flex justify-center space-x-3 mt-2">
                  <p><i class="fa-solid fa-star mr-1 text-yellow-500"></i>{{ store.rating }}</p>
                  <p><i class="fa-solid fa-clock mr-1 text-gray-500"></i>{{ store.operating_hours }}</p>
                </div>
                <div class="flex justify-center space-x-3 mb-2 mt-1">
                  <p><i class="fa-solid fa-phone mr-1 text-blue-600"></i>{{ store.phone_number }}</p>
                  <p><span class="mr-1 font-bold">리뷰</span>{{ store.reviews }}</p>
                </div>
                <p class="mb-2"><i class="fa-solid fa-location-dot mr-1 text-red-500"></i>{{ store.address }}</p>
                <p>{{ store.description }}</p>
                <div class="mt-3">
                  <button @click="gotoManageStore({store, index})" class="bg-gray-100 w-[150px] p-2 rounded-md text-sm hover:bg-gray-200 font-bold">가게 관리</button>
                </div>
              </div>
            </div>
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
        if (imageurl.startsWith("http://localhost:8000/media/images")) {
          return imageurl; // 기존 URL 유지
        }
        if (imageurl.startsWith("http://localhost:8000/media/")) {
          return imageurl.replace("/media/", "/media/images/");
        }
        return imageurl
      }
      // 상대 경로라면 `http://localhost:8000`을 붙여서 반환
      return `http://localhost:8000${imageurl}`;
    },
    generatecode(number) {
      // 공통된 문자열을 기반으로 랜덤한 코드 리스트 생성
      const prefix = 'WEKRJLD'

      // 한 자리 숫자일 경우 앞에 0을 붙이기
      const formattedNumber = String(number).padStart(2, '0'); 

      // 최종 코드 생성
      const unique_code = prefix + formattedNumber

      return unique_code
    }
  }
}
</script>