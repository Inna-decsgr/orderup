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
        <button type="submit">저장</button>
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
    }
  },
  data() {
    return {
      form: { ...this.menu }, // 사용자 정보를 기반으로 초기화
      originalMenu: { ...this.menu },
    }
  },
}

</script>