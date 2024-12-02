<template>
  <div>
    <h4>리뷰쓰기</h4>
    <div>
      <p><strong>{{ order.restaurant.name }}</strong></p>
      <div class="star-rating">
        <div class="stars">
          <i
            v-for="star in 5" 
            :key="star" 
            class="fa fa-star"
            :class="{'active': isFullStar(star) || (hoveredStar >= star)}"
            @mouseover="hoverRating(star)"
            @mouseleave="clearHover"
            @click="setRating(star)"
          ></i><span v-if="rating !== 0">{{ rating }}</span>
        </div>
        
      </div>
      <div>
        <button @click="showFileInput = !showFileInput">사진 첨부하기</button>
        <input 
          v-if="showFileInput"
          type="file"
          accept="image/*"
          @change="handleFileUpload"
        >
        <div v-if="this.imagePreview">
          <img :src="this.imagePreview" alt="이미지 미리보기" style="width:300px; height:200px">
        </div>
      </div>
      <div>
        <textarea
          placeholder="음식의 맛, 양, 포장 상태 등 음식에 대한 솔직한 리뷰를 남겨주세요.(선택사항)"
          rows="4"
          cols="50"
          style="resize: vertical;"
        ></textarea>
      </div>
      <button>완료</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      rating: 0,  // 클릭된 최종 별점
      hoveredStar: 0,  // 사용자가 마우스 호버 중인 별
      showFileInput: false,
      uploadedFile: null,
      imageFile: null,
    };
  },
  computed: {
    order() {
      return this.$store.getters.getOrder;
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
        const reader = new FileReader();
        reader.onload = (e) => {
          this.imagePreview = e.target.result;
          console.log('미리보기 URL',this.imagePreview);
        };
        reader.readAsDataURL(this.uploadedFile);
      }
    }
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
  padding: 5px;
}

.stars {
  display: flex;
  justify-content: center;
}

.stars .fa {
  font-size: 30px;
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