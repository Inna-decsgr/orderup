<template>
  <button @click="toggleLike">
    <i :class="`fa-${isactive ? 'solid' : 'regular'} fa-heart`"></i>
  </button>
  <!--{{ this.isactive }}
  {{ store.id || store.store_id }}
  {{ user.id }}
  {{ this.likedstore }}-->
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      isactive: false
    }
  },
  computed: {
    user() {
      return this.$store.getters.getUser;
    },
    store() {
      return this.$store.getters.getStore;
    },
    likedstore() {
      return this.$store.getters.getLikedStore;
    }
  }, 
  mounted() {
    if (Array.isArray(this.likedstore) && this.likedstore.includes(this.store.id || this.store.store_id)) {
      this.isactive = true;
    }
  },
  methods: {
    async toggleLike() {
      try {
        const csrfResponse = await axios.get("http://localhost:8000/order/csrftoken/");
        const csrfToken = csrfResponse.data.csrfToken;

        const response = await axios.post(`http://localhost:8000/order/changelike/${this.user.id}/`, { storeid: this.store.id || this.store.store_id }, {
          headers: {
            'X-CSRFToken': csrfToken,
          }
        });

        if (response.data.is_active) {
          this.$store.commit('addStoreToLiked', this.store.id || this.store.store_id);
        } else {
          this.$store.commit('removeStoreFromLiked', this.store.id || this.store.store_id);
        }

        // isactive 상태 업데이트 (하트 아이콘을 위한 상태)
        this.isactive = response.data.is_active;
      } catch (error) {
        console.error("Error toggling like:", error);
      }
    },
  }
}
</script>