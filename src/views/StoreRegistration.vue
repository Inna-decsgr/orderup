<template>
  <form @submit.prevent="submitForm">
    <div>
      <label for="restaurantName">가게 이름</label>
      <input type="text" v-model="restaurant.name" id="restaurantName" required>
    </div>
    <div>
      <label for="restaurantAddress">주소</label>
      <input type="text" v-model="restaurant.address" id="restaurantAddress" required>
    </div>
    <div>
      <label for="restaurantPhoneNumber">전화번호</label>
      <input type="text" v-model="restaurant.phone_number" id="restaurantPhoneNumber" required>
    </div>
    <div>
      <label for="restaurantRating">평점</label>
      <input type="text" v-model="restaurant.rating" id="restaurantRating" required>
    </div>
    <div>
      <label for="restaurantOwner">소유주</label>
      <input type="text" v-model="restaurant.owner" id="restaurantOwner" required>
    </div>
    <div>
      <label for="categories">카테고리를 선택하세요</label>
      <div v-for="category in categories" :key="category.id">
        <input type="checkbox" :value="category.id" v-model="selectedCategories">
        <label>{{ category.text }}</label>
      </div>
    </div>
    <div>
      <label for="restaurantOperatingHours">운영 시간</label>
      <input type="text" v-model="restaurant.operating_hours" id="restaurantOperatingHours" required>
    </div>
    <div>
      <label for="restaurantDescription">상단에 표시할 가게 설명을 작성해주세요</label>
      <input type="text" v-model="restaurant.description" id="restaurantDescription" required>
    </div>
    <div>
      <label for="restaurantImage">대표 사진</label>
      <input type="text" v-model="restaurant.image_url" id="restaurantImage" required>
    </div>
    <div>
      <label for="restaurantDeliveryFee">배달료</label>
      <input type="text" v-model="restaurant.delivery_fee" id="restaurantDeliveryFee" required>
    </div>
    <button type="submit" @click="registrationstore">등록하기</button>
  </form>
</template>

<script>
import { mapGetters } from 'vuex';
import axios from 'axios';

export default {
  data() {
    return {
      restaurant: {
        name: '',
        address: '',
        phone_number: '',
        rating: '',
        owner: '',
        operating_hours: '',
        description: '',
        image_url: '',
        delivery_fee: ''
      },
      categories: [
        { id: 1, text: 'Fast Food' },
        { id: 2, text: 'Chinese' },
        { id: 3, text: 'Snack Food' },
        { id: 4, text: 'Japanese' },
        { id: 5, text: 'Dessert' },
        { id: 6, text: 'Asian' },
        { id: 7, text: 'Western Food' },
      ],
      selectedCategories: [],
    };
  },
  computed: {
    ...mapGetters(['getUser']),
    user() {
      return this.getUser;
    },
  },
  methods: {
    async registrationstore() {
      const formData = {
        name: this.restaurant.name,
        address: this.restaurant.address,
        phone_number: this.restaurant.phone_number,
        rating: this.restaurant.rating,
        owner: this.user.id,
        categories: this.selectedCategories,
        operating_hours: this.restaurant.operating_hours,
        description: this.restaurant.description,
        image_url: this.restaurant.image_url,
        delivery_fee: this.restaurant.delivery_fee
      };

      console.log("Submitting form data:", formData); // 디버깅 출력
      console.log('selectedCategories', this.selectedCategories);

      // 여기에 API 호출을 통해 백엔드에 데이터 전송
      const csrfResponse = await axios.get("http://localhost:8000/order/csrftoken/");
      const csrfToken = csrfResponse.data.csrfToken;

      try {
        const response = await axios.post('http://localhost:8000/order/storeregis/', formData, {
          headers: {
            'X-CSRFToken': csrfToken,  
          }
        });
        console.log(response.data);
      } catch (error) {
        if (error.response) {
          console.log("API error:", error.response.data); // 오류 메시지 출력
        } else {
          console.log("Error occurred:", error.message);
        }
}
      
    },
  },
};
</script>
