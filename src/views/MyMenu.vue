<template>
  <div>
    <p>가게 관리하기 - Store ID: {{ storeid }}</p>
    <div>
      <p>메뉴판</p>
      <button @click="ShowForm">메뉴 등록</button>
      <NewMenu v-if="this.NewForm" :cancel="cancel" :storeid="storeid"/>
      <div v-for="(menu, index) in menus" :key="index">
        <div v-if="EditNumber === index">
          <EditMenu :menu="menu" :canceledit="cancelEdit" :getMenu="fetchStoreMenu"/>
        </div>
        <div v-else>
          <button @click="editmode(index)">수정</button>
          <button @click="deletemenu(menu.id)">삭제</button>
          <p>{{ menu.name }}</p>
          <p>{{ menu.description }}</p>
          <p>가격 {{ Math.floor(menu.price) }}원</p>
          <img :src="menu.image_url" alt="Menu Image" />
          <div v-for="optionGroup in menu.option_groups" :key="optionGroup.group_name">
            <p>{{ optionGroup.group_name }}</p>
            <ul>
              <li v-for="item in optionGroup.items" :key="item.name">
                {{ item.name }} - {{ Math.floor(item.price) }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NewMenu from '../components/NewMenu.vue'
import EditMenu from '../components/EditMenu.vue'
import axios from 'axios';

export default {
  components: {
    NewMenu,
    EditMenu
  },
  data() {
    return {
      NewForm: false,
      menus: [],
      EditNumber: null
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
    },
    async deletemenu(menuid) {
      const response = await axios.get(`http://localhost:8000/order/deletemenu/${menuid}/`);
      console.log(response.data);
      alert('메뉴가 성공적으로 삭제되었습니다.')
      this.fetchStoreMenu();
    },
    editmode(index) {
      this.EditNumber = index
    },
    cancelEdit() {
      this.EditNumber = null
    }
  }
}
</script>