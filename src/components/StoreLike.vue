<template>
  가게 찜
  <button @click="toggleLike">
    <i :class="`fa-${this.isactive ? 'solid' : 'regular'} fa-heart`"></i>
  </button>
  {{ this.isactive }}
  {{ storeid }}
  {{ user.id }}
</template>

<script>
import { mapGetters } from 'vuex';
import axios from 'axios';

export default {
  data() {
    return {
      isactive: false
    }
  },
  props: {
    storeid: {
      type: Number,
      required: true
    }
  },
  mounted() {
    //this.getStoreLike()
  },
  computed: {
    ...mapGetters(['getUser']),
    user() {
      return this.getUser;
    },
  },
  methods: {
    async getStoreLike() {
      await axios.get(`http://localhost:8000/order/getstorelikes/${this.user.id}/`, { storeid: this.storeid });
    },

    async toggleLike() {
      try {
        const csrfResponse = await axios.get("http://localhost:8000/order/csrftoken/");
        const csrfToken = csrfResponse.data.csrfToken;

        const response = await axios.post(`http://localhost:8000/order/changelike/${this.user.id}/`, { storeid: this.storeid }, {
          headers: {
            'X-CSRFToken': csrfToken,
          }
        });
        this.isactive = response.data.is_active;
      } catch (error) {
        console.error("Error toggling like:", error);
      }
    }
  }
}
</script>