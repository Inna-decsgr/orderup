<template>
  <div>
    <form>
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
    <button type="submit" @click="editReview(localReviews[0].id)">완료</button>
    <button @click="cancel">취소</button>
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
        this.cancel();
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