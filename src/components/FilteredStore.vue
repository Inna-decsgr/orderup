<template>
  <div>
    <div v-if="filteredstore && filteredstore.length">
      <div v-for="store in filteredstore" :key="store.id" style="cursor:pointer">
        <h3 @click="detailstore({id:store.id, name: store.name})">{{ store.name }}</h3>
        <StoreLike :storeid="store.id"/>
        <p>{{ store.address }}</p>
        <p>{{ store.phonenumber }}</p>
        <p>{{ store.rating }}</p>
        <p>{{ store.description }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import StoreLike from '../components/StoreLike.vue'

export default {
  components: {
    StoreLike
  },
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