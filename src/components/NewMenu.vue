<template>
  <div class=" border p-2 rounded-sm">
    <div class="flex justify-between items-center mb-3">
      <p class="font-bold pl-4">메뉴 추가</p>
      <div>
        <button @click="submitForm" class="bg-gray-100 py-1 px-2 text-sm rounded-sm mr-2 hover:bg-gray-200">완료</button>
        <button @click="handleCancel" class="bg-gray-100 py-1 px-2 text-sm rounded-sm hover:bg-gray-200">취소</button>
      </div>
    </div>
    <form @submit.prevent="submitForm">
      <div class="pb-2">
        <label for="menuName" class="font-bold mr-2 text-sm w-[100px] text-center">메뉴명</label>
        <input 
          type="text" 
          v-model="menu.name" 
          class="border rounded-sm outline-none w-[250px] text-sm"
          required
        >
      </div>
      <div class="flex items-center pb-2">
        <label for="menuDescription" class="font-bold mr-2 text-sm w-[100px] text-center">설명</label>
        <textarea 
          v-model="menu.description" 
          id="menuDescription" 
          class="border rounded-sm outline-none w-[300px] h-[80px] text-sm"
          required
        ></textarea>
      </div>
      <div class="pb-2">
        <label for="menuPrice" class="font-bold mr-2 text-sm w-[100px] text-center">가격</label>
        <input 
          type="number" 
          v-model="menu.price" 
          id="menuPrice"
          class="border rounded-sm outline-none w-[300px] pl-2"
          required
          >
      </div>
      <div>
        <label for="menuimage" class="font-bold mr-2 text-sm w-[100px] text-center">메뉴 사진</label>
        <input 
          type="file" 
          id="menuimage" 
          @change="handleImageUpload" 
          class="hidden"
        >
        <label for="menuimage" class="cursor-pointer inline-block py-1 px-2 bg-gray-200 rounded-full">
          <i class="fa-solid fa-camera"></i>
        </label>
        <div v-if="imagePreview">
          <img :src="imagePreview" alt="이미지 미리보기" class="w-[300px] h-[200px] rounded-sm mx-auto mt-3">
        </div>
      </div>
      <div class="flex justify-between items-center pt-5">
        <p class="font-bold pl-4">상세 옵션 추가</p>
        <button @click.prevent="addOptionsGroup" class="text-sm bg-gray-100 py-1 px-2 rounded-sm hover:bg-gray-200">옵션 그룹 추가</button>
      </div>
      <div v-for="(optionGroup, groupIndex) in optionsGroups" :key="groupIndex">
        <label class="font-bold text-sm w-[110px] text-center">옵션 그룹</label>
        <input 
          type="text" 
          v-model="optionGroup.name"
          class="border rounded-sm outline-none w-[300px] my-3 text-sm pl-2" 
          placeholder="ex) 음료"
          required
        >
        <div class="flex items-center text-sm">
          <p class="font-bold text-sm w-[110px] text-center">옵션 항목</p>
          <button @click.prevent="addOption(optionGroup)" class="text-sm bg-gray-100 py-1 px-2 rounded-sm hover:bg-gray-200">옵션 추가</button>
        </div>
        <div v-for="(option, optionIndex) in optionGroup.options" :key="optionIndex" class="pl-6">
          <div class="flex justify-between items-center">
            <div>
              <input 
                type="text" 
                v-model="option.name" 
                placeholder="옵션 이름 ex) 제로 콜라"
                class="border rounded-sm outline-none w-[300px] text-sm pl-2 mt-3 mb-2" 
                required
              ><br/>
              <input 
                type="text" 
                v-model="option.price" 
                placeholder="옵션 가격 ex) 1500원" 
                class="border rounded-sm outline-none w-[300px] text-sm pl-2" 
                required
              >
            </div>
            <button @click="removeOption(optionGroup, optionIndex)" class="mr-3 bg-gray-100 py-1 px-2 text-sm hover:bg-gray-200">삭제</button>
          </div>
        </div>
      </div>
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
        price: ''
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