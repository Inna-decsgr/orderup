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
        <label for="restaurantImage">대표 사진</label>
        <input type="text" v-model="menu.image_url" id="menuImage" required>
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

      <button @click="submitForm">메뉴 등록</button>
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
        image_url: ''
      },
      optionsGroups: []
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
    }
  },
  methods: {
    async submitForm() {
      // 메뉴 등록 로직 구현
      const FormData = {
        ...this.menu,
        options: this.optionsGroups
      }

      // 서버에 요청 보내기
      console.log('메뉴 등록', FormData);
      try {
        const csrfResponse = await axios.get("http://localhost:8000/order/csrftoken/");
        const csrfToken = csrfResponse.data.csrfToken;
        const response = await axios.post(`http://localhost:8000/order/newmenu/${this.storeid}/`, FormData, {
          headers: {
            'X-CSRFToken': csrfToken,
          }
        });

        console.log('메뉴 등록 성공', response.data);
        alert('메뉴가 등록되었습니다.');

        // 수정 모드 해제해서 수정 컴포넌트 감추기
        this.cancel();
      } catch (error) {
        console.error('메뉴 등록 중 오류 발생:', error);
      }
    },
    addOptionsGroup() {
      // 새로운 옵션 그룹 추가
      this.optionsGroups.push({
        name: '',
        options: []
      });
    },
    addOption(optionGroup) {
      // 선택된 옵션 그룹에 옵션 항목 추가
      optionGroup.options.push({
        name: '',
        price: 0
      });
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
        image_url: '',
      };
      this.optionsGroups = []
    }
  }
}
</script>