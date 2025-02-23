<template>
  <div class="mt-3">
    <div class="flex mb-3 justify-center w-full">
      <input 
        type="text" 
        class="border-1 rounded-l-lg w-full p-2 outline-none" 
        placeholder="먹고 싶은 메뉴나 가게를 찾아보세요" 
        v-model="keyword"
        @keyup.enter="goResultPage"
      />
      <button class="border-[1px] border-l-0 rounded-r-lg px-3 flex-shrink-0" @click="goResultPage" :disabled="!keyword.trim()">
        <i class="fa-solid fa-magnifying-glass"></i>
      </button>
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
      // 검색 기록에 저장하기
      this.$store.commit('setSearchKeyword', this.keyword);
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