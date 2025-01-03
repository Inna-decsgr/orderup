<template>
  <div class="mt-3">
    <div class="flex mb-3 justify-center w-full">
      <input 
        type="text" 
        class="border-1 rounded-l-lg w-full p-2" 
        placeholder="찾는 메뉴가 뭐예요?" 
        v-model="keyword"
        @keyup.enter="goResultPage"
      />
      <button class="border-[1px] border-l-0 rounded-r-lg p-2 flex-shrink-0" @click="goResultPage" :disabled="!keyword.trim()">검색</button>
    </div>
  </div>
</template>

<script>

export default {
  data() {
    return {
      keyword: '',
    }
  },
  methods: {
    async goResultPage() {
      this.$router.push({
        path: '/searchresult',
        query: {
          keyword: this.keyword
        }
      })
    }
  }
}
</script>