<template>
  <div class="bg-gray-100">
    <div class="flex items-center p-3 bg-white">
      <button @click="this.$router.push('/orderlist')"><i class="fa-solid fa-arrow-left mr-3"></i></button>
      <p class="text-lg font-bold">주문내역</p>
    </div>
    <div class="bg-white p-3">
      <p class="text-violet-500 font-bold text-sm">{{ getStatusMessage(orderdata.status) }}</p>
      <p v-if="orderdata.restaurant" class="text-lg font-bold pt-1">{{ orderdata.restaurant.name }}</p>
      <p v-if="orderdata.items && orderdata.items.length > 0" class="font-bold text-sm pb-1">
        {{ orderdata.items[0].menu_name }} {{ orderdata.items.length > 1 ? `외 ${orderdata.items.length - 1}개` : `${orderdata.items[0].quantity}개` }}
      </p>
      <p v-if="orderdata.discount_amount > 0" class="border-1 border-violet-500 w-[100px] text-center py-1 px-2 text-xs rounded-xl font-bold mb-3 mt-1"><span class="text-violet-500">{{ Number(orderdata.discount_amount).toLocaleString() }}</span>원 할인</p>
      <p v-if="orderdata.ordered_at" class="text-sm text-gray-400 font-semibold">주문일시 : {{ formattedDate(orderdata.ordered_at) }}</p>
      <p class="text-sm text-gray-400 font-semibold">주문번호 : {{ generateOrderId(Number(orderdata.id)) }}</p>
      <p class="font-bold bg-gray-100 text-[10px] w-[90px] text-center py-[3px] mt-1 rounded-xl">현금영수증 보기</p>
      <button class="border w-full p-2 rounded-md font-bold mt-4 text-sm"><i class="fa-solid fa-headset pr-2"></i>도움이 필요하신가요?</button>
    </div>
    <div class="p-3 bg-white mt-3">
      <ul v-for="menu in orderdata.items" :key="menu.menu_id" class="my-2">
        <li class="font-bold text-sm">{{ menu.menu_name }} {{ menu.quantity }}개</li>
        <p class="flex items-center text-sm text-gray-500">
          <i class="fa-solid fa-circle text-[4px] mx-1 text-gray-400"></i>
          기본 {{ menu.price.toLocaleString() }}원
        </p>
        <div v-if="menu.options">
          <div v-for="option in menu.options" :key="option.name">
            <p>{{ option.name }} ({{ option.price.toLocaleString() }}원)</p>
          </div>
        </div>
      </ul>
      <p class="font-bold pt-2">{{ Number(orderdata.total_price).toLocaleString() }}원</p>
    </div>
    <div class="p-3 bg-white mt-3">
      <div class="flex justify-between items-center font-bold mb-1">
        <p>총 금액</p>
        <p v-if="orderdata.restaurant">{{ Number(orderdata.total_price + orderdata.restaurant.delivery_fee).toLocaleString() }}원</p>
      </div>
      <div class="flex justify-between items-center text-sm text-gray-500 mb-1">
        <p>메뉴금액</p>
        <p>{{ Number(orderdata.total_price).toLocaleString() }}원</p>
      </div>
      <div class="flex justify-between items-center text-sm text-gray-500 mb-3">
        <p>배달팁</p>
        <p v-if="orderdata.restaurant">{{ Number(orderdata.restaurant.delivery_fee).toLocaleString() }}원</p>
      </div>
      <div v-if="orderdata.discount_amount > 0" class="flex justify-between items-center font-bold pb-3 border-b mb-3">
        <p>할인금액</p>
        <p class="text-violet-500">-{{ Number(orderdata.discount_amount).toLocaleString() }}원</p>
      </div>
      <div class="flex justify-between items-center font-bold mb-1">
        <p>총 결제금액</p>
        <p v-if="orderdata.restaurant">{{Number(orderdata.final_price) > 0 
          ? Number(orderdata.final_price).toLocaleString() 
          : Number(orderdata.total_price + orderdata.restaurant.delivery_fee).toLocaleString()
        }}원</p>
      </div>
      <div class="flex justify-between items-center text-sm text-gray-500">
        <p>결제 방법</p>
        <p>{{ orderdata.payment_method }}</p>
      </div>
    </div>
    <div class="p-3 bg-white mt-3 text-sm">
      <p class="font-bold">배달주소</p>
      <p class="text-gray-500 pb-3 mb-3 border-b">{{ this.user.address }}</p>
      <p class="font-bold">전화번호</p>
      <p class="text-gray-500">{{ this.user.phone_number }}</p>
    </div>
    <div class="p-3 bg-white mt-3">
      <button @click="detailstore({id:orderdata.restaurant.id, name: orderdata.restaurant.name})" class="w-full bg-violet-500 font-bold text-white rounded-md p-3 text-sm">같은 메뉴 담으러 가기</button>
    </div>
  </div>
</template>


<script>
import axios from 'axios';
import { formatDate } from '@/utils/dateutils';


export default {
  data() {
    return {
      orderid: null,
      orderdata: {}
    }
  },
  computed: {
    user() {
      return this.$store.getters.getUser;
    },
    store() {
      return this.$store.getters.getStore;
    }
  },
  created() {
    this.orderid = this.$route.params.orderid;
  },
  mounted() {
    this.getDetailorder();
  },
  methods: {
    async getDetailorder() {
      const response = await axios.get(`http://localhost:8000/order/getorderdetail/${this.orderid}/`);
      console.log('가게 상세 데이터', response.data);
      this.orderdata = response.data
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
      console.log("변환 전 날짜:", date);
      return formatDate(date);
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
    detailstore(store) {
      this.$router.push('/detailstore'),
      this.$store.commit('setStore', store);
    },
  }
}
</script>