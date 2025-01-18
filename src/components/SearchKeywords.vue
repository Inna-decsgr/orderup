<template>
  <div class="mt-3">
    <p class="font-bold text-sm my-2">최근 검색어</p>
    <ul class="flex gap-2">
      <li v-for="keyword in uniqueSearchKeywords" :key="keyword" class="flex items-center border py-1 pl-3 pr-[10px] text-xs font-bold rounded-xl">
        {{ keyword }}<i class="fa-solid fa-x text-[10px] pl-[5px] cursor-pointer" @click="removeKeyword(keyword)"></i>
      </li>
    </ul>
  </div>
</template>

<script>

export default {
  computed: {
    uniqueSearchKeywords() {
      // 중복 제거한 검색 키워드들
      return [...new Set(this.$store.getters.getSearchKeywords)];
    }
  },
  methods: {
    removeKeyword(keyword) {
      this.$store.commit('removekeyword', keyword);
    }
  }

}
</script>