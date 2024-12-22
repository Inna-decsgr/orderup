<template>
  가게 찜
  <button @click="toggleLike">
    <i :class="`fa-${isactive ? 'solid' : 'regular'} fa-heart`"></i>
  </button>
  {{ this.isactive }}
  {{ storeid }}
  {{ user.id }}
  {{ this.likedstore }}
</template>

<script>
import { mapGetters } from 'vuex';
import axios from 'axios';

export default {
  data() {
    return {
      isactive: Array.isArray(this.likedstore) && this.likedstore.includes(this.storeid) ? true : false
    }
  },
  props: {
    storeid: {
      type: Number,
      required: true
    },
    likedstore: {
      type: Array,
      required: true,
      default: () => []
    }
  },
  computed: {
    ...mapGetters(['getUser']),
    user() {
      return this.getUser;
    },
  },
  methods: {
    async toggleLike() {
      try {
        const csrfResponse = await axios.get("http://localhost:8000/order/csrftoken/");
        const csrfToken = csrfResponse.data.csrfToken;

        const response = await axios.post(`http://localhost:8000/order/changelike/${this.user.id}/`, { storeid: this.storeid }, {
          headers: {
            'X-CSRFToken': csrfToken,
          }
        });

        if (response.data.is_active) {
          this.$store.commit('addStoreToLiked', this.storeid);
        } else {
          this.$store.commit('removeStoreFromLiked', this.storeid);
        }

        // isactive 상태 업데이트 (하트 아이콘을 위한 상태)
        this.isactive = response.data.is_active;
      } catch (error) {
        console.error("Error toggling like:", error);
      }
    }
  }
}
</script>