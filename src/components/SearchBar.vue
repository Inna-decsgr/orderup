<template>
  <div>
    <div class="input-group mb-3">
      <input 
        type="text" 
        class="form-control" 
        placeholder="검색어를 입력해주세요" 
        v-model="keyword"
        @keyup.enter="goResultPage"
      />
      <button class="btn btn-outline-secondary" type="button" @click="goResultPage" :disabled="!keyword.trim()">검색</button>
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