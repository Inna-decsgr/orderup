<template>
  <div>
    <h2>가게 수정</h2>
    <div>
      <button @click="updateStore">수정</button>
      <button @click="handleCancel">취소</button>
      <form @submit.prevent="updateStore">
        <label for="storename">가게 이름</label>
        <input 
          type="text"
          id="storename"
          v-model="form.name"
          class="form-control"
          required
        >
        <label for="storenumber">가게 전화번호</label>
        <input 
          type="text"
          id="storenumber"
          v-model="form.phone_number"
          class="form-control"
          required
        >
        <label for="storedescription">가게 설명</label>
        <input 
          type="text"
          id="storedescription"
          v-model="form.description"
          class="form-control"
          required
        >
        <div>
          <label for="storeimage">가게 이미지</label>
          <input
            type="file"
            id="storeimage"
            @change="handleImageUpload"
          />
          <div v-if="imagePreview">
            <img :src="imagePreview" alt="이미지 미리보기" style="width:300px; height:200px;">
          </div>
        </div>
        <label for="storeaddress">가게 주소</label>
        <input 
          type="text"
          id="storeaddress"
          v-model="form.address"
          class="form-control"
          required
        >
        <label for="storehours">가게 운영시간</label>
        <input 
          type="text"
          id="storehours"
          v-model="form.operating_hours"
          class="form-control"
          required
        >
        <label for="storerating">가게 평점</label>
        <input 
          type="text"
          id="storerating"
          v-model="form.rating"
          class="form-control"
          required
        >
        <label for="storedeliveryfee">배달료</label>
        <input 
          type="text"
          id="storedeliveryfee"
          v-model="form.delivery_fee"
          class="form-control"
          required
        >
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
    handleCancel() {
      this.cancel();
    },
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
        alert('정보 수정이 성공적으로 완료되었습니다.')
        this.$router.push('/mystore');
        this.cancel();
      } catch (error) {
        console.error('가게 정보 수정 실패', error);
      }
    }
  }

}
</script>