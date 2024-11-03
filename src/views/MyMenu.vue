<template>
  <div>
    <p>가게 관리하기 - Store ID: {{ storeid }}</p>
    <div>
      <p>메뉴판</p>
      <div v-for="menu in menus" :key="menu.id" style="background-color: plum;">
        <button>수정</button>
        <button>삭제</button>
        <p>{{ menu.name }}</p>
        <p>{{ menu.description }}</p>
        <p>{{ Math.floor(menu.price) }}</p>
        <img :src="menu.image_url" alt="Menu Image" />
        <div v-for="optionGroup in menu.option_groups" :key="optionGroup.group_name">
          <h3>{{ optionGroup.group_name }}</h3>
          <ul>
            <li v-for="item in optionGroup.items" :key="item.name">
              {{ item.name }} - {{ Math.floor(item.price) }}
            </li>
          </ul>
        </div>
      </div>
    </div>
    <button @click="ShowForm">메뉴 등록</button>
    <NewMenu v-if="this.NewForm" :cancel="cancel" :storeid="storeid"/>
  
  </div>
</template>

<script>
import NewMenu from '../components/NewMenu.vue'
import axios from 'axios';

export default {
  components: {
    NewMenu
  },
  data() {
    return {
      NewForm: false,
      menus: [],
    }
  },
  computed: {
    storeid() {
      return this.$route.query.storeid;
    }
  },
  mounted() {
    this.fetchStoreMenu();
  },
  methods: {
    ShowForm() {
      this.NewForm = true;
    },
    cancel() {
      this.NewForm = false;
    },
    async fetchStoreMenu() {
      console.log('메뉴 정보 모두 불러오기', this.storeid)

      try {
        // 이미지 파일과 함께 수정 데이터 전송
        //const csrfResponse = await axios.get("http://localhost:8000/order/csrftoken/");
        //const csrfToken = csrfResponse.data.csrfToken;

        const response = await axios.get(`http://localhost:8000/order/getmenus/${this.storeid}/`)
        console.log('메뉴 정보 불러오기 성공', response.data);
        this.menus = response.data;
        console.log('불러온 메뉴들 정보', this.menus);
      } catch (error) {
        console.error('메뉴 정보 불러오기 실패', error);
      }
    }
  }
}
</script>