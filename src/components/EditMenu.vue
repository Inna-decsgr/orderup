<template>
  <div>
    <div v-if="menu" class="relative p-3 text-sm border mt-3 rounded-sm">
      <form @submit.prevent="updateMenu" class="form-label">
        <label for="menuname" class="font-bold pb-1">메뉴명</label>
        <input 
          type="text" 
          id="menuname" 
          v-model="form.name"
          class="border block py-1 px-2 w-[400px] rounded-sm mb-3"
          required 
        />
        <label for="description" class="font-bold pb-1">메뉴 설명</label>
        <textarea
          id="description" 
          v-model="form.description" 
          class="border block py-1 px-2 w-[400px] rounded-sm mb-3"
          required 
        ></textarea>
        <label for="price" class="font-bold pb-1">가격</label>
        <input 
          type="number" 
          id="price" 
          v-model="form.price" 
          class="border block py-1 px-2 w-[400px] rounded-sm mb-3"
          required 
        />
        <div class="mb-2">
          <label for="menuimage" class="font-bold pb-1">대표 이미지</label><br/>
          <input
            type="file"
            id="menuimage"
            @change="handleImageUpload"
            class="hidden"
          />
          <label for="menuimage" class="cursor-pointer inline-block py-1 px-2 bg-gray-200 rounded-full">
            <i class="fa-solid fa-camera"></i>
          </label>
          <div v-if="imagePreview">
            <img :src="imagePreview" alt="이미지 미리보기" class="w-[300px] h-[200px] mt-2">
          </div>
        </div>
        <div class="absolute bottom-3 right-3">
          <button @click="editMenu" class="bg-violet-500 text-white py-1 px-2 rounded-md text-sm font-bold mr-2 hover:bg-violet-600">저장</button>
          <button @click="canceledit" class="bg-violet-500 text-white py-1 px-2 rounded-md text-sm font-bold hover:bg-violet-600">취소</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    menu: {
      type: Object,
      required: true
    },
    canceledit: {
      type: Function,
      required: true
    },
    getMenu: {
      type: Function,
      required: true
    }
  },
  data() {
    return {
      form: { ...this.menu }, // 사용자 정보를 기반으로 초기화
      originalMenu: { ...this.menu },
      imageFile: null,
      imagePreview: this.menu.image_url
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
    async editMenu() {
      const menuData = new FormData();

      menuData.append('name', this.form.name);
      menuData.append('description', this.form.description);
      menuData.append('price', this.form.price);
      if (this.imageFile) {
        menuData.append('image', this.imageFile);
      }
      console.log('요청 데이터', menuData);

      try {
        // CSRF 토큰 요청
        const csrfResponse = await axios.get("http://localhost:8000/order/csrftoken/");
        const csrfToken = csrfResponse.data.csrfToken;

        const response = await axios.put(`http://localhost:8000/order/updatemenu/${this.menu.id}/`, menuData, {
          headers: {
            'X-CSRFToken': csrfToken,  
          }
        });

        this.menus = response.data;
        console.log(this.menus);
        alert('메뉴가 성공적으로 수정되었습니다.');
        this.canceledit();
        this.getMenu();
      } catch (error) {
        if (error.response && error.response.status === 400) {
          this.errorMessage = error.response.data.message || '내 가게 정보를 불러오는 데 실패했습니다.';
        } else {
          this.errorMessage = '서버와의 통신에 문제가 발생했습니다.';
        }
        console.error('메뉴 수정 가져오기 실패', error);
      }
    }
  }
}

</script>