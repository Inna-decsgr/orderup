<template>
  <div>
    가게 상세 페이지
    <p>가게 아이디: {{ storeid }}</p>

    <div v-if="menus.length > 0">
      <h3>메뉴판</h3>
      <div v-for="menu in menus" :key="menu.id">
        <p>{{ menu.name }}</p>
        <p>{{ menu.description }}</p>
        <p>{{ menu.price }}</p>
        <img v-if="menu.image_url" :src="menu.image_url" alt="Menu Image" style="width: 400px; height: 300px;">
        <!--옵션 그룹이 있을 경우 출력-->
        <div v-if="menu.option_groups && menu.option_groups.length > 0">
          <div v-for="optionGroup in menu.option_groups" :key="optionGroup.group_name">
            <p>{{ optionGroup.group_name }}</p>
            <ul>
              <li v-for="optionItem in optionGroup.items" :key="optionItem.name">
                {{ optionItem.name }} - {{ optionItem.price }} 원
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      menus: []
    }
  },
  computed: {
    storeid() {
      return this.$route.query.storeid;
    }
  },
  mounted() {
    this.getMenus(this.storeid);
  },
  methods: {
    async getMenus(storeid) {
      const response = await axios.get(`http://localhost:8000/order/getmenus/${storeid}/`)
      this.menus = response.data
      console.log('가게 메뉴들', this.menus);
    }
  }
}
</script>