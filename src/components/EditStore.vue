<template>
  <div>
    <div class="flex justify-between items-center py-3">
      <p class="font-bold">기본 정보 수정</p>
      <div>
        <button @click="updateStore" class="bg-violet-500 text-white py-1 px-2 text-xs rounded-sm">완료</button>
      </div>
    </div>
    <div>
      <form @submit.prevent="updateStore" class="text-sm">
        <div class="mb-2">
          <label for="storename" class="font-bold pb-1">상호명</label><br/>
          <input 
            type="text"
            id="storename"
            v-model="form.name"
            class="border py-1 px-2 block w-[400px] rounded-md"
            required
          >
        </div>
        <div class="mb-2">
          <label for="storenumber" class="font-bold pb-1">전화번호</label>
          <input 
            type="text"
            id="storenumber"
            v-model="form.phone_number"
            class="border py-1 px-2 block w-[400px] rounded-md"
            required
          >
        </div>
        <div class="mb-2">
          <label for="storedescription" class="font-bold pb-1">설명</label>
          <textarea
            id="storedescription"
            v-model="form.description"
            class="border py-1 px-2 block w-[400px] h-[100px] rounded-md outline-none"
            required
          ></textarea>
        </div>
        <div class="mb-2">
          <label for="storeimage" class="font-bold pb-1">대표 이미지</label><br/>
          <input
            type="file"
            id="storeimage"
            @change="handleImageUpload"
            class="hidden"
          />
          <label for="storeimage" class="cursor-pointer inline-block py-1 px-2 bg-gray-200 rounded-full">
            <i class="fa-solid fa-camera"></i>
          </label>
          <div v-if="imagePreview">
            <img :src="imagePreview" alt="이미지 미리보기" class="w-[300px] h-[200px] mt-2">
          </div>
        </div>
        <div class="mb-2">
          <label for="storeaddress" class="font-bold pb-1">주소</label>
          <input 
            type="text"
            id="storeaddress"
            v-model="form.address"
            class="border py-1 px-2 block w-[400px] rounded-md"
            required
          >
        </div>
        <div class="mb-2">
          <label for="storehours" class="font-bold pb-1">운영시간</label>
          <input 
            type="text"
            id="storehours"
            v-model="form.operating_hours"
            class="border py-1 px-2 block w-[400px] rounded-md"
            required
          >
        </div>
        <div class="mb-2">
          <label for="storerating" class="font-bold pb-1">평점</label>
          <input 
            type="text"
            id="storerating"
            v-model="form.rating"
            class="border py-1 px-2 block w-[400px] rounded-md"
            required
          >
        </div>
        <div class="mb-2">
          <label for="storedeliveryfee" class="font-bold pb-1">배달료</label>
          <input 
            type="text"
            id="storedeliveryfee"
            v-model="form.delivery_fee"
            class="border py-1 px-2 block w-[400px] rounded-md"
            required
          >
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    store: {
      type: Object,
      required: true
    },
    cancel: {
      type: Function,
      required: true
    },
  },
  data() {
    return {
      form: { ...this.store },
      originalStore: {...this.store},
      imageFile: null,
      imagePreview: this.store.image_url
    }
  },
  methods: {
    handleImageUpload(event) {
      console.log(event.target.files);
      const file = event.target.files[0];
      if (file) {
        this.imageFile = file;

        // 미리보기 이미지 생성
        const reader = new FileReader();
        reader.onload = (e) => {
          this.imagePreview = e.target.result;
          console.log(this.imagePreview);
        };
        reader.readAsDataURL(file);
      }
    },
    async updateStore() {
      try {
        const formData = new FormData();

        // 가게 수정 데이터에 이미지 파일 포함
        formData.append('name', this.form.name);
        formData.append('phone_number', this.form.phone_number);
        formData.append('description', this.form.description);
        formData.append('address', this.form.address);
        formData.append('operating_hours', this.form.operating_hours);
        formData.append('rating', this.form.rating);
        formData.append('delivery_fee', this.form.delivery_fee);
        if (this.imageFile) {
          formData.append('image', this.imageFile); // 이미지가 있을 경우에만 추가
        }
        console.log('요청 데이터', formData)


        // 이미지 파일과 함께 수정 데이터 전송
        const csrfResponse = await axios.get("http://localhost:8000/order/csrftoken/");
        const csrfToken = csrfResponse.data.csrfToken;

        const response = await axios.put(`http://localhost:8000/order/editstore/${this.store.id}/`, formData, {
          headers: {
            'X-CSRFToken': csrfToken,
          }
        })
        console.log('가게 정보 수정 성공', response.data);
        this.$router.push('/mystore/allmystores');
        this.cancel();
      } catch (error) {
        console.error('가게 정보 수정 실패', error);
      }
    }
  }

}
</script>