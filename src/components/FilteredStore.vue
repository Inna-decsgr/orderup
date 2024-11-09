<template>
  <div>
    <div v-if="filteredstore && filteredstore.length">
      <div v-for="store in filteredstore" :key="store.id" @click="detailstore(store.id)" style="cursor:pointer">
        <h3>{{ store.name }}</h3>
        <p>{{ store.address }}</p>
        <p>{{ store.phonenumber }}</p>
        <p>{{ store.rating }}</p>
        <p>{{ store.description }}</p>
      </div>
    </div>
    <div v-else>
      <p>No stores found</p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    filteredstore: {
      type: Array,
      required: true
    }
  },
  methods: {
    detailstore(storeid) {
      this.$router.push({
        path: '/detailstore',
        query: {
          storeid: storeid
        }
      })
    }
  }
}
</script>