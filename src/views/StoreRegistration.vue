<template>
  <div :class="{ 'blur-background': registersuccess }">
    <div class="flex justify-between items-center py-2">
      <div class="text-lg font-bold py-3">
        <p>오더업 입점에 필요한</p>
        <p>정보를 채워주세요</p>
      </div>
      <button @click="gotomyStore" class="pr-[50px]">
        <i class="fa-solid fa-x"></i>
      </button>
    </div>
    <form @submit.prevent="submitForm" class="text-sm">
      <div>
        <label for="restaurantName" class="font-bold pr-3 w-[80px] text-center mb-3">상호명</label>
        <input 
          type="text" 
          v-model="restaurant.name" 
          id="restaurantName" 
          class="border w-[350px] py-1 px-2 rounded-md outline-none"
          required
        >
      </div>
      <div>
        <label for="restaurantAddress" class="font-bold pr-3 w-[80px] text-center mb-3">주소</label>
        <input 
          type="text" 
          v-model="restaurant.address" 
          id="restaurantAddress" 
          class="border w-[350px] py-1 px-2 rounded-md outline-none"
          required
        >
      </div>
      <div>
        <label for="restaurantPhoneNumber" class="font-bold pr-3 w-[80px] text-center mb-3">전화번호</label>
        <input 
          type="text" 
          v-model="restaurant.phone_number" 
          id="restaurantPhoneNumber" 
          class="border w-[350px] py-1 px-2 rounded-md outline-none"
          required
        >
      </div>
      <div>
        <label for="restaurantRating" class="font-bold pr-3 w-[80px] text-center mb-3">평점</label>
        <input 
          type="text" 
          v-model="restaurant.rating" 
          id="restaurantRating" 
          required
          class="border w-[350px] py-1 px-2 rounded-md outline-none"
        >
      </div>
      <div>
        <label for="restaurantOwner" class="font-bold pr-3 w-[80px] text-center mb-3">소유주</label>
        <input 
          type="text" 
          v-model="restaurant.owner" 
          id="restaurantOwner" 
          required
          class="border w-[350px] py-1 px-2 rounded-md outline-none"
        >
      </div>
      <div>
        <label for="restaurantOperatingHours" class="font-bold pr-3 w-[80px] text-center mb-3">운영 시간</label>
        <input 
          type="text" 
          v-model="restaurant.operating_hours" 
          id="restaurantOperatingHours" 
          required
          class="border w-[350px] py-1 px-2 rounded-md outline-none"
        >
      </div>
      <div>
        <label for="restaurantImage" class="font-bold w-[80px] text-center mr-3 mb-3">대표 이미지</label>
        <input 
          type="file" 
          id="restaurantImage" 
          @change="handleImageUpload" 
          accept="image/*"
          class="hidden"
        >
        <!-- ✅ 카메라 아이콘 (클릭 시 파일 선택) -->
        <label for="restaurantImage" class="cursor-pointer inline-block py-1 px-2 bg-gray-200 rounded-full">
          <i class="fa-solid fa-camera"></i>
        </label>
        <!-- ✅ 이미지 미리보기 -->
        <div v-if="imagePreview">
          <img :src="imagePreview" alt="미리보기" class="w-[300px] h-[200px] mb-3">
        </div>
      </div>
      <div class="mb-3">
        <label for="categories" class="font-bold text-center mb-3">가게 분류</label>
        <div class="grid grid-cols-5 gap-2 px-2">
          <div v-for="category in categories" :key="category.id" class="flex items-center">
            <input 
              type="checkbox" 
              :value="category.id" 
              v-model="selectedCategories"
              class="mr-2"
            >
            <label>{{ category.text }}</label>
          </div>
        </div>
      </div>
      <div>
        <label for="restaurantDescription" class="font-bold text-center mb-2 mr-2">상단에 표시할 가게 설명을 작성해주세요</label>
        <textarea
          v-model="restaurant.description" 
          id="restaurantDescription" 
          required
          class="border w-[430px] py-1 px-2 rounded-md outline-none mb-3"
        ></textarea>
      </div>
      <div>
        <label for="restaurantDeliveryFee" class="font-bold pr-3 w-[80px] text-center mb-3">배달료</label>
        <input 
          type="text" 
          v-model="restaurant.delivery_fee" 
          id="restaurantDeliveryFee" 
          required
          class="border w-[350px] py-1 px-2 rounded-md outline-none mb-3"
        >
      </div>
      <button type="submit" @click="registrationstore" class="w-full bg-violet-500 p-2 rounded-md mb-[50px] font-bold text-white mt-5">입점 신청하기</button>
    </form>
  </div>
  <div v-if="registersuccess" class="text-center py-5 px-[30px] border w-[450px] rounded-md transition-opacity duration-500 fixed bg-black text-white text-sm shadow-lg transform -translate-x-1/2 -translate-y-1/2 top-1/3 left-1/2">
    <i class="fa-solid fa-circle-check text-green-500 text-5xl mb-3"></i>
    <p class="text-2xl font-bold mb-4">입점 신청 완료</p>
    <div class="font-bold text-[15px] my-3">
      <p>입력한 정보는 검토 후 승인되며,</p>
      <p>승인 후 오더업 앱에 노출돼요.</p>
    </div>
    <div class="text-[12px] mb-5 text-gray-300">
      <p>광고 시작일은 승인 진행상황에 따라 선택한 시작희망일과</p>
      <p>다를 수 있으며, 승인된 정보는 셀프서비스를 통해</p>
      <p>언제든지 변경할 수 있어요.</p>
    </div>

    <button @click="gotomyStore" class="font-bold border-b border-gray-300 pb-[1px] text-gray-300">오더업사장님광장 메인으로</button>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import axios from 'axios';

export default {
  data() {
    return {
      restaurant: {
        name: '',
        address: '',
        phone_number: '',
        rating: '',
        owner: '',
        operating_hours: '',
        description: '',
        image_url: '',
        delivery_fee: ''
      },
      categories: [
        { id: 1, text: '패스트푸드' },
        { id: 2, text: '중식' },
        { id: 3, text: '분식' },
        { id: 4, text: '일식' },
        { id: 5, text: '카페·디저트' },
        { id: 6, text: '아시안' },
        { id: 7, text: '양식' },
        { id: 8, text: '피자' },
        { id: 9, text: '족발·보쌈' },
        { id: 10, text: '찜·탕'}
      ],
      selectedCategories: [],
      imageFile: null,
      imagePreview: null,
      registersuccess: false
    };
  },
  computed: {
    ...mapGetters(['getUser']),
    user() {
      return this.getUser;
    },
  },
  watch: {
    registersuccess(value) {
      console.log('registersuccess', this.registersuccess);
      if (value) {
        document.body.style.overflow = "hidden";
      } else {
        document.body.style.overflow = "auto";
      }
    }
  },
  methods: {
    async registrationstore() {
      const formData = new FormData();

      formData.append("name", this.restaurant.name);
      formData.append("address", this.restaurant.address);
      formData.append("phone_number", this.restaurant.phone_number);
      formData.append("rating", this.restaurant.rating);
      formData.append("owner", this.user.id);
      formData.append("categories", JSON.stringify(this.selectedCategories));
      formData.append("operating_hours", this.restaurant.operating_hours);
      formData.append("description", this.restaurant.description);
      formData.append("delivery_fee", this.restaurant.delivery_fee);
      formData.append("image_url", this.restaurant.image_url); // ✅ 기존 URL도 전송

      if (this.imageFile) {
        formData.append("image", this.imageFile);
      }

      console.log("Submitting form data:", formData); // 디버깅 출력
      console.log('selectedCategories', this.selectedCategories);

      // 여기에 API 호출을 통해 백엔드에 데이터 전송
      const csrfResponse = await axios.get("http://localhost:8000/order/csrftoken/");
      const csrfToken = csrfResponse.data.csrfToken;

      try {
        const response = await axios.post('http://localhost:8000/order/storeregis/', formData, {
          headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'multipart/form-data'
          }
        });
        console.log(response.data);
        this.registersuccess = true;
      } catch (error) {
        if (error.response) {
          console.log("API error:", error.response.data); // 오류 메시지 출력
        } else {
          console.log("Error occurred:", error.message);
        }
      }
    },
    handleImageUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.imageFile = file;

        const reader = new FileReader();
        reader.onload = (e) => {
          this.imagePreview = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },
    gotomyStore() {
      this.$router.push('/mystore');
      console.log('registersuccess', this.registersuccess);
      this.registersuccess = false;
    }
  },
};
</script>


<style>
.blur-background {
  filter: blur(2px) !important;
  pointer-events: none;
  transition: filter 0.3s ease-in-out;
}
</style>