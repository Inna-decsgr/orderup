<template>
  <div class="p-4">
    <p class="font-bold text-lg">평가 및 리뷰 작성</p>
    <div>
      <p class="font-bold mt-3">{{ order.restaurant.name }}</p>
      <div class="star-rating">
        <div class="stars">
          <i
            v-for="star in 5" 
            :key="star" 
            class="fa fa-star mt-2 mb-4"
            :class="{'active': isFullStar(star) || (hoveredStar >= star)}"
            @mouseover="hoverRating(star)"
            @mouseleave="clearHover"
            @click="setRating(star)"
          ></i>
        </div>
        
      </div>
      <div class="flex mb-4">
        <input 
          type="file"
          id="reviewimage"
          @change="handleFileUpload"
          class="hidden"
        />
        <label for="reviewimage" class="cursor-pointer text-center flex flex-col justify-center border p-2 text-xs font-bold mr-2" @click="showFileInput = !showFileInput">
          <i class="fas fa-camera text-xl text-gray-600"></i>
          <p>사진 추가</p>
        </label>
        <div v-if="imagePreview">
          <img :src="imagePreview" alt="이미지 미리보기" class="w-[100px]">
        </div>
      </div>
      <div>
        <textarea
          v-model="reviewText"
          placeholder="음식의 맛, 양, 포장 상태 등 음식에 대한 솔직한 리뷰를 남겨주세요.(선택사항)"
          rows="4"
          cols="50"
          class="border text-sm p-2 rounded-md outline-none"
        ></textarea>
      </div>
      <button @click="submitReview" class="font-bold bg-violet-500 text-white w-full py-1 px-2 rounded-sm mt-5 text-sm">완료</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      rating: 0,  // 클릭된 최종 별점
      hoveredStar: 0,  // 사용자가 마우스 호버 중인 별
      showFileInput: false,
      uploadedFile: null,
      imagePreview: null,
      imageFile: null,
      storeid: null,
      reviewText: ""
    };
  },
  computed: {
    order() {
      return this.$store.getters.getOrder;
    },
    store() {
      return this.$store.getters.getStore;
    },
    user() {
      return this.$store.getters.getUser;
    }
  },
  methods: {
    setRating(star) {
      // 별 클릭했을 때 최종 점수 설정
      this.rating = star;
    },
    hoverRating(star) {
      // 마우스 호버 시 별점 업데이트
      this.hoveredStar = star;
    },
    clearHover() {
      // 마우스가 별 영역에서 벗어나면 초기화
      this.hoveredStar = 0;
    },
    isFullStar(star) {
      // 완전히 채워진 별 표시 조건
      return star <= this.rating;
    },
    isHalfStar(star) {
      // 반만 채워진 별 표시 조건
      return star <= this.hoveredStar;
    },
    handleFileUpload(event) {
      console.log(event.target.files)
      this.uploadedFile = event.target.files[0];
      console.log('업로드된 파일:', this.uploadedFile);

      if (this.uploadedFile) {
        this.imageFile = this.uploadedFile;
        const reader = new FileReader();
        reader.onload = (e) => {
          this.imagePreview = e.target.result;
          console.log('미리보기 URL',this.imagePreview);
        };
        reader.readAsDataURL(this.uploadedFile);
      }
    },
    async submitReview() {
      this.storeid = this.order.restaurant.id;
      console.log(this.storeid);
      const csrfResponse = await axios.get("http://localhost:8000/order/csrftoken/");
      const csrfToken = csrfResponse.data.csrfToken;

      const formData = new FormData();
      formData.append("rating", this.rating);
      formData.append("userid", this.user.id)
      formData.append("review", this.reviewText);
      formData.append("orderid", this.order.order_id)

      if (this.uploadedFile) {
        formData.append("image", this.uploadedFile);
      }

      try {
        const response = await axios.post(`http://localhost:8000/order/newreview/${this.storeid}/`, formData, {
          headers: {
            'X-CSRFToken': csrfToken,
            "Content-Type": "multipart/form-data",
          }
        });
        console.log(response.data);
        alert("리뷰 등록이 완료되었습니다. 소중한 리뷰를 남겨주셔서 감사합니다.")
        this.$router.push('/')

      } catch (error) {
        console.error('리뷰 등록 중 오류 발생:', error)
      }
    },
  }
}
</script>

<style scoped>
body {
  font-family: 'Noto Sans KR', sans-serif;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.star-rating {
  width: 250px;
  text-align: center;
  border-radius: 5px;
}

.stars {
  display: flex;
}

.stars .fa {
  font-size: 20px;
  color: #ccc; /* 기본 별 색상 */
  cursor: pointer;
}

.stars .fa.active,
.stars .fa:hover {
  color: rgb(250, 215, 19);
  /*text-shadow: 0 0 5px rgb(230, 204, 62);*/
}

.stars .fa:hover ~ .fa {
  color: #ccc; /* 마우스 호버 후의 나머지 별 색상 */
}


</style>