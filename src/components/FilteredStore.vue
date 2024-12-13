<template>
  <div>
    <div v-if="filteredstore && filteredstore.length">
      <div v-for="store in filteredstore" :key="store.id" >
        <h3 @click="detailstore({id:store.id, name: store.name})" style="cursor:pointer">
          {{ store.name }}
        </h3>
        <StoreLike :storeid="store.id" :likedstore="this.likedstore" />
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
import { mapGetters } from 'vuex';
import axios from 'axios';

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
  computed: {
    ...mapGetters(['getUser']),
    user() {
      return this.getUser;
    },
  },
  mounted() {
    this.getStoreLike()
  },
  methods: {
    async getStoreLike() {
      const stores = await axios.get(`http://localhost:8000/order/getstorelikes/${this.user.id}/`, { storeid: this.storeid });
      console.log(stores.data);
      this.likedstore = stores.data.likes.map(like => like.store_id);
      console.log('가게 아이디들', this.likedstore);
      
    },
    detailstore(store) {
      this.$router.push('/detailstore'),
      this.$store.commit('setStore', store);
    }
  }
}
</script>