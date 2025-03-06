<template>
  <div class="px-4 py-3">
    <div class="flex items-center">
      <button @click="cancel"><i class="fa-solid fa-x pr-3 text-xs pb-1"></i></button>
      <p class="font-bold pl-[170px]">평가 및 리뷰 작성</p>
    </div>
    <form>
      <div class="my-2">
        <p class="font-bold">{{ store.name }}</p>
        <div class="stars">
          <i
            v-for="star in 5"
            :key="star" 
            class="fa fa-star"
            :class="{'active': star <= localReviews[0].rating}"
            @click="updateRating(star)"
          ></i>
          <span v-if="currentRating !== 0" class="ratingscore font-bold text-xs">{{ currentRating }}</span>
        </div>
      </div>
      <div>
        <textarea
          id="reviewcontent"
          v-model="localReviews[0].content"
          required
          rows="4"
          cols="40"
          class="border-2 border-gray-300 p-3 text-sm font-bold"
        ></textarea>
      </div>
      <div class="flex">
        <input 
          type="file"
          id="reviewimage"
          @change="handleImageEdit"
          class="hidden"
        />
        <label for="reviewimage" class="cursor-pointer text-center flex flex-col justify-center border p-2 text-xs font-bold mr-2">
          <i class="fas fa-camera text-xl text-gray-600"></i>
          <p>사진 추가</p>
        </label>
        <div v-if="imagePreview">
          <img :src="imagePreview" alt="이미지 미리보기" class="w-[100px]">
        </div>
      </div>
    </form>
    <button type="submit" @click="editReview(localReviews[0].id)" class="bg-violet-500 text-white font-bold w-full text-sm p-2 mt-3 rounded-md">완료</button>
  </div>
</template>

<script>
import axios from 'axios';

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
  computed: {
    store() {
      return this.$store.getters.getStore;
    }
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
    async editReview(reviewid) {
      const reviewData = {
        content: this.localReviews[0].content,
        rating: this.currentRating,
        image: this.imageFile || this.localReviews[0].image_url
      };

      console.log('수정된 리뷰 데이터', reviewData);

      const formData = new FormData();
      formData.append('content', reviewData.content);
      formData.append('rating', reviewData.rating);

      // 이미지가 변경되면 새 이미지로 없으면 기존 이미지 사용
      if (reviewData.image) {
        formData.append('image', reviewData.image);
      }

      try {
        const csrfResponse = await axios.get("http://localhost:8000/order/csrftoken/");
        const csrfToken = csrfResponse.data.csrfToken;
        
        const response = await axios.put(`http://localhost:8000/order/editmyreview/${reviewid}/`, formData, {
          headers: {
            'X-CSRFToken': csrfToken,
          }
        });
        console.log('서버 응답', response.data);
        this.$router.push('/orderlist')
      } catch (error) {
        console.error('리뷰 수정 중 오류', error);
        alert('리뷰 수정 중 오류가 발생했습니다.')
      }
    },
    updateRating(star) {
      this.currentRating = star;
      this.localReviews[0].rating = star;
    }
  }
}
</script>