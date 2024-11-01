<template>
  <div>
    <p>가게 관리하기 - Store ID: {{ storeid }}</p>
    <div>
      <p>메뉴판</p>
    </div>
    <button @click="ShowForm">메뉴 등록</button>
    <NewMenu v-if="this.NewForm" :cancel="cancel" :storeid="storeid"/>
  
  </div>
</template>

<script>
import NewMenu from '../components/NewMenu.vue'

export default {
  components: {
    NewMenu
  },
  data() {
    return {
      NewForm: false,
    }
  },
  computed: {
    storeid() {
      return this.$route.query.storeid;
    }
  },
  methods: {
    ShowForm() {
      this.NewForm = true;
    },
    cancel() {
      this.NewForm = false;
    }
  }
}
</script>