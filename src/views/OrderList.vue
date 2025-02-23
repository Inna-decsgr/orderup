<template>
  <div>
    <div class="p-3">
      <div class="flex items-center">
        <i class="fa-solid fa-arrow-left pr-4 cursor-pointer" @click="gotohome"></i>
        <p class="font-bold text-xl">주문 내역</p>
      </div>
      <p class="font-bold mt-3 pl-8">배달·포장</p>
    </div>
    <div v-if="orderlist.length > 0" class="px-3">
      <div v-for="order in orderlist" :key="order.order_id" class="mb-3">
        <div>
          <div class="flex justify-between items-center pt-1 pb-2">
            <p class="font-bold text-sm text-violet-700">{{ getStatusMessage(order.status) }}</p>
            <button v-if="order.status === 'pending'" @click="cancelorder(order.order_id)" class="font-bold text-sm border-1 border-violet-700 py-1 px-2 rounded-md text-violet-700">주문 취소</button>
          </div>
          <div v-if="order.review === true">
            <p>후기 작성완료</p>
            <button @click="gotoMyReview(order.restaurant)">후기 보러가기</button>
          </div>
          <p v-if="order.status === 'accepted'">
            <i class="fa-solid fa-fire-burner"></i>
            음식을 맛있게 조리하고 있습니다
          </p>
          <button v-if="order.status === 'delivering'" @click="showLocation(order.order_id)">배달 현황보기</button>
          <div v-if="showDelivering[order.order_id]" class="popup">
            <RiderLocation :cancel="closepopup" :orderid="order.order_id" @confirm="handleConfirm(order.order_id)"/>
          </div>
          <h5><strong>{{ order.restaurant.name }}</strong></h5>
          <div v-for="item in order.items" :key="item.order_item_id">
            <p>{{ item.menu.name }} {{ item.quantity }}개</p>
          </div>
          <br/>
          <p>주문 일시: {{ formattedDate(order.ordered_at) }}</p>
          <p>주문 번호: {{ generateOrderId(order.order_id) }}</p>

          <div>
            상세 내역
            <div v-for="item in order.items" :key="item.order_item_id">
              <strong>{{ item.menu.name }} {{ item.quantity }}개</strong>
              <li>기본: {{ item.menu.price.toLocaleString() }}원</li>
              <li v-for="option in item.options" :key="option.name">
                {{ option.name}} ({{ option.price.toLocaleString() }}원)
              </li>
            </div>
            <p>{{ order.total_price.toLocaleString() }}원</p>
          </div>

          <div>
            <p><strong>결제 금액</strong></p>
            <p>주문 금액 : {{ order.total_price.toLocaleString() }}원</p>
            <p>배달비 {{ order.restaurant.deliveryfee }}원</p>
            <p v-if="order.discount_amount">쿠폰 적용 : - {{ order.discount_amount }}원</p>
            <p>
              총 결제금액 
              <span v-if="order.discount_amount" class="originalprice">{{ (Number(order.total_price) + Number(order.restaurant.deliveryfee)).toLocaleString() }}원</span> {{ (Number(order.total_price) + Number(order.restaurant.deliveryfee)
              - Number(order.discount_amount)).toLocaleString() }}원
            </p>
            <p>결제방법 {{ order.payment_method }}</p>
          </div>
          <button v-if="order.review === false && order.status === 'delivered'" @click="gotoReview(order)">후기 작성하기</button>
        </div>
        <hr />
      </div>
    </div>
    <div v-else class="text-center pt-[100px] px-[60px]">
      <p class="font-bold">주문 내역이 없어요.</p>
      <p class="text-gray-500 text-sm pt-2">비회원 주문내역은 30일동안 확인 가능합니다. 오더업 회원 탈퇴하시면 비회원 주문내역을 확인할 수 있습니다.</p>
      <button @click="gotofilteredStore" class="bg-violet-400 w-[200px] p-2 text-white text-sm font-bold my-5 rounded-md">주문하러 가기</button>
    </div>
    <div class="py-3 px-12">
      <p class="font-bold">재주문 많은 가게를 추천해요</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import {reactive} from 'vue'

import { formatDate } from '../utils/dateutils';
import RiderLocation from '../components/RiderLocation.vue'

export default {
  data() {
    return {
      orderlist: [],
      showDelivering: reactive({}),
    }
  },
  components: {
    RiderLocation
  },
  computed: {
    user() {
      return this.$store.getters.getUser;
    },
    store() {
      return this.$store.getters.getStore;
    }
  },
  mounted() {
    this.getOrderList();
  },
  methods: {
    async getOrderList() {
      //alert('사용자 id에 맞는 주문 내역 가져오기');
      console.log(this.user.id)
      const orders = await axios.get(`http://localhost:8000/order/getorderlist/${this.user.id}`);
      this.orderlist = orders.data.sort((a, b) => new Date(b.ordered_at) - new Date(a.ordered_at));
      console.log('주문 내역들', this.orderlist);
    },
    getStatusMessage(status) {
      switch (status) {
        case 'pending':
          return '주문이 완료되었어요';
        case 'accepted':
          return '주문이 수락되었어요';
        case 'delivering':
          return '배달원이 음식을 픽업하고 배달중이에요💨';
        case 'delivered':
          return '배달이 완료되었어요';
        case 'canceled':
          return '주문이 취소되었어요';
        case 'rejected':
          return '주문이 거절되었어요';
        default:
          return '상태 정보 없음';
      }
    },
    generateOrderId(orderid) {
      // 주문 아이디를 12자리로 포맷, 앞에 0을 채우고 접두사 'T1VI' 추가
      const paddedId = orderid.toString().padStart(8, '0'); // 숫자를 문자열로 바꾸고 12자리로 패딩
      return `T1VI${paddedId}`;
    },
    formattedDate(date) {
      return formatDate(date);
    },
    async cancelorder(orderid) {
      const isConfirmed = window.confirm('주문을 취소하시겠습니까?');

      if (isConfirmed) {
        const csrfResponse = await axios.get("http://localhost:8000/order/csrftoken/");
        const csrfToken = csrfResponse.data.csrfToken;
        
        console.log(orderid);
        const response = await axios.put(`http://localhost:8000/order/cancelorder/${orderid}/`, null, {
          headers: {
            'X-CSRFToken': csrfToken,
          }
        });
        console.log(response.data);
        this.getOrderList();
      }
    },
    gotofilteredStore(category) {
      this.$router.push('/filteredstore');
      this.$store.commit('setCategory', category.name);
    },
    showLocation(orderid) {
      this.showDelivering[orderid] = true 
    },
    closepopup(orderid) {
      this.showDelivering[orderid] = false
    },
    async handleConfirm(orderid) {
      console.log('확인 버튼 클릭됨! orderlist에서 처리')
      const csrfResponse = await axios.get("http://localhost:8000/order/csrftoken/");
        const csrfToken = csrfResponse.data.csrfToken;
        
        console.log(orderid);
        const response = await axios.put(`http://localhost:8000/order/completedelivery/${orderid}/`, null, {
          headers: {
            'X-CSRFToken': csrfToken,
          }
        });
      console.log(response.data);
      this.getOrderList();
    },
    gotoReview(order) {
      console.log(order);
      this.$router.push('/newreview');
      this.$store.commit('setOrder', order)
    },
    gotoMyReview(store) {
      this.$router.push('/myreview');
      this.$store.commit('setStore', store)
    },
    gotohome() {
      this.$router.push('/')
    }
  }
}
</script>

<style>
.popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.2);
  display: flex;
  justify-content: center;
  align-items: center;
}

.originalprice{
  color: gray;
  text-decoration: line-through;
}
</style>