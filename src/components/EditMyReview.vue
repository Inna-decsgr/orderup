<template>
  <div>
    <form @submit.prevent="editReview">
      <div>
        <label for="reviewcontent">리뷰 내용</label><br/>
        <textarea
          id="reviewcontent"
          v-model="localReviews[0].content"
          required
          rows="5"
          cols="40"
        ></textarea>
      </div>
      <div>
        <label for="reviewimage">리뷰 사진</label>
        <div v-if="imagePreview">
          <img :src="imagePreview" alt="이미지 미리보기" style="width:300px; height:200px;">
        </div>
        <input 
          type="file"
          id="reviewimage"
          @change="handleImageEdit"
        />
      </div>
      <div>
        <label for="reviewrating">리뷰 평점</label>
        <div class="stars">
            <i
              v-for="star in 5"
              :key="star" 
              class="fa fa-star"
              :class="{'active': star <= localReviews[0].rating}"
              @click="updateRating(star)"
            ></i>
            <span v-if="currentRating !== 0" class="ratingscore">{{ currentRating }}</span>
          </div>
      </div>
    </form>
    <button @click="editReview">완료</button>
    <button @click="cancel">취소</button>
  </div>
</template>

<script>

export default {
  props: {
    cancel: {
      type: Function,
      required: true
    },
    reviews: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      localReviews: [...this.reviews],
      imageFile: null,
      imagePreview: this.reviews[0]?.image_url || null,
      currentRating: this.reviews[0]?.rating || null
    };
  },
  methods: {
    handleImageEdit(event) {
      const file = event.target.files[0];
      console.log(file);

      if (file) {
        this.imageFile = file;

        const reader = new FileReader();
        reader.onload = (e) => {
          this.imagePreview = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },
    updateRating(star) {
      this.currentRating = star;
      this.localReviews[0].rating = star;
    }
  }
}
</script>