<template>
  <div>
    <div v-if="filteredstore && filteredstore.length">
      <div v-for="store in filteredstore" :key="store.id" @click="detailstore({id:store.id, name: store.name})" style="cursor:pointer">
        <h3>{{ store.name }}</h3>
        <p>{{ store.address }}</p>
        <p>{{ store.phonenumber }}</p>
        <p>{{ store.rating }}</p>
        <p>{{ store.description }}</p>
      </div>
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
    detailstore(store) {
      this.$router.push('/detailstore'),
      this.$store.commit('setStore', store);
    }
  }
}
</script>