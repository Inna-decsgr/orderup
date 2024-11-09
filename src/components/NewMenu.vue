<template>
  <div style="background-color: aliceblue;">
    새 메뉴 등록
    <form @submit.prevent="submitForm">
      <div>
        <label for="menuName">메뉴명</label>
        <input type="text" v-model="menu.name" required>
      </div>
      <div>
        <label for="menuDescription">설명</label>
        <input type="text" v-model="menu.description" id="menuDescription" required>
      </div>
      <div>
        <label for="menuPrice">가격</label>
        <input type="number" v-model="menu.price" id="menuPrice" required>
      </div>
      <div>
        <label for="menuimage">가게 이미지</label>
        <input 
          type="file" 
          id="menuimage" 
          @change="handleImageUpload" 
          required
        >
        <div v-if="imagePreview">
          <img :src="imagePreview" alt="이미지 미리보기" style="width:300px; height:200px;">
        </div>
      </div>
      <h3>상세 옵션 추가</h3>
      <div v-for="(optionGroup, groupIndex) in optionsGroups" :key="groupIndex">
        <label>옵션 그룹 이름</label>
        <input type="text" v-model="optionGroup.name" required>
        <h4>옵션 항목</h4>
        <div v-for="(option, optionIndex) in optionGroup.options" :key="optionIndex">
          <input type="text" v-model="option.name" placeholder="옵션 이름" required>
          <input type="number" v-model="option.price" placeholder="옵션 가격" required>
          <button @click="removeOption(optionGroup, optionIndex)">삭제</button>
        </div>
        <button @click.prevent="addOption(optionGroup)">옵션 추가</button>
      </div>
      <button @click.prevent="addOptionsGroup">옵션 그룹 추가</button>

      <button>메뉴 등록</button>
      <button @click="handleCancel">취소</button>
    </form> 
  </div>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      menu: {
        name: '',
        description: '',
        price: 0,
      },
      optionsGroups: [],
      imageFile: null,
      imagePreview: null
    }
  },
  props: {
    storeid: {
      type: String,
      required: true
    },
    cancel: {
      type: Function,
      required: true
    },
    getmenu: {
      type: Function,
      required: true
    }
  },
  methods: {
    handleImageUpload(event) {
      console.log(event.target.files);
      const file = event.target.files[0];
      if (file) {
        this.imageFile = file;

        const reader = new FileReader();
        reader.onload = (e) => {
          this.imagePreview = e.target.result;
          console.log(this.imagePreview);
        };
        reader.readAsDataURL(file);
      }
    },
    addOptionsGroup() {
      // 새로운 옵션 그룹 추가
      this.optionsGroups.push({
        name: '',
        options: []
      });
      console.log('this.optionsGroups', this.optionsGroups)
    },
    addOption(optionGroup) {
      // 선택된 옵션 그룹에 옵션 항목 추가
      optionGroup.options.push({
        name: '',
        price: 0
      });
      console.log('optionGroup.options', optionGroup.options); 
    },
    removeOption(optionGroup, index) {
      // 선택된 옵션 항목 삭제
      optionGroup.options.splice(index, 1);
    },
    handleCancel() {
      this.cancel();
      this.menu = {
        name: '',
        description: '',
        price: 0,
      };
      this.optionsGroups = [],
      this.imageFile = null;
      this.imagePreview = null;
    },
    async submitForm() {
      console.log(this.optionsGroups)
      const formData = new FormData();
      formData.append("name", this.menu.name);
      formData.append("description", this.menu.description);
      formData.append("price", this.menu.price);

      if (this.imageFile) {
        formData.append("image", this.imageFile);
      }

      formData.append("options", JSON.stringify(this.optionsGroups));
      console.log("전송할 formData의 내용:");
      for (let pair of formData.entries()) {
        console.log(`${pair[0]}: ${pair[1]}`);
      }
      
      try {
        const csrfResponse = await axios.get("http://localhost:8000/order/csrftoken/");
        const csrfToken = csrfResponse.data.csrfToken;
        const response = await axios.post(`http://localhost:8000/order/newmenu/${this.storeid}/`, formData, {
          headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'multipart/form-data',
          }
        });

        console.log('메뉴 등록 성공', response.data);
        alert('메뉴가 등록되었습니다.');
        this.handleCancel();  // 수정 모드 해제해서 수정 컴포넌트 감추기
        this.getmenu();
      } catch (error) {
        console.error('메뉴 등록 중 오류 발생:', error);
      }
    }
  }
}
</script>