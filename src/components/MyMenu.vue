<template>
  <div>
    <div class="relative">
      <div v-if="!this.NewForm" class="flex items-center">
        <p class="font-bold text-sm">단품 메뉴</p>
        <button @click="ShowForm" class="absolute right-0 bg-blue-500 text-white p-2 rounded-sm ml-auto text-xs hover:bg-blue-600">메뉴 추가</button>
      </div>
      <NewMenu v-if="this.NewForm" :cancel="cancel" :storeid="store.id" :getmenu="fetchStoreMenu" />
      <div v-for="(menu, index) in menus" :key="index">
        <div v-if="EditNumber === index">
          <EditMenu :menu="menu" :canceledit="cancelEdit" :getMenu="fetchStoreMenu"/>
        </div>
        <div v-else class="flex justify-center border-b pt-3">
          <div class="flex basis-4/5 py-3 pr-2">
            <img :src="menu.image_url" alt="Menu Image" class="w-[80px] h-[80px] object-contain rounded-l pr-3" />
            <div class="text-sm">
              <p class="font-bold">{{ menu.name }}</p>
              <p class="text-xs py-1">{{ menu.description }}</p>
              <p class="text-xs font-bold">{{menu.price.toLocaleString() }}원</p>
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
          <div class="flex justify-center items-center basis-1/5">
            <button @click="editmode(index)" class="bg-gray-100 rounded-sm w-[50px] mr-1 h-[30px] text-xs hover:bg-gray-200">수정</button>
            <button @click="deletemenu(menu.id)" class="bg-gray-100 rounded-sm w-[50px] h-[30px] text-xs hover:bg-gray-200">삭제</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NewMenu from './NewMenu.vue'
import EditMenu from './EditMenu.vue'
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
  mounted() {
    this.fetchStoreMenu();
  },
  methods: {
    ShowForm() {
      this.NewForm = true;
    },
    async fetchStoreMenu() {
      console.log('메뉴 정보 모두 불러오기', this.storeid)

      try {
        const csrfResponse = await axios.get("http://localhost:8000/order/csrftoken/");
        const csrfToken = csrfResponse.data.csrfToken;

        const response = await axios.get(`http://localhost:8000/order/getmenus/${this.store.id}/`, {
          headers: {
            'X-CSRFToken': csrfToken,  // 수정된 부분
          }
        })
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