<template>
  <div>
    <h2>메뉴 수정</h2>
    <div v-if="menu">
      <form @submit.prevent="updateMenu" class="form-label">
        <label for="menuname">메뉴명</label>
        <input 
          type="text" 
          id="menuname" 
          v-model="form.name"
          class="form-control"
          required 
        />
        <label for="description" class="form-label">메뉴 설명</label>
        <input 
          type="text" 
          id="description" 
          v-model="form.description" 
          class="form-control"
          required 
        />
        <label for="price" class="form-label">가격</label>
        <input 
          type="number" 
          id="price" 
          v-model="form.price" 
          class="form-control"
          required 
        />
        <div>
          <label for="menuimage">메뉴 이미지</label>
          <input
            type="file"
            id="menuimage"
            @change="handleImageUpload"
          />
          <div v-if="imagePreview">
            <img :src="imagePreview" alt="이미지 미리보기" style="width:300px; height:200px;">
          </div>
        </div>
        <button @click="editMenu">저장</button>
        <button @click="canceledit">취소</button>
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