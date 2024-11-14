<template>
  <div>
    <h3><strong>주문 내역</strong></h3>
    <div v-for="order in orderlist" :key="order.order_id">
      <div>
        <p>{{ getStatusMessage(order.status) }}</p>
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
            <li>기본: {{ item.menu.price }}원</li>
            <li v-for="option in item.options" :key="option.name">
              {{ option.name}} ({{ option.price }}원)
            </li>
          </div>
          <p>{{ order.total_price }}원</p>
        </div>

        <div>
          <p>결제 금액</p>
          <p>주문 금액 {{ order.total_price }}원</p>
          <p>배달팁 {{ order.restaurant.deliveryfee }}</p>
          <br/>
          <p>총 결제 금액 <strong>{{ order.total_price + order.restaurant.deliveryfee }}원</strong></p>
          <p>결제방법 {{ order.payment_method }}</p>
        </div>
      </div>
      <hr />
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { formatDate } from '../utils/dateutils';

export default {
  data() {
    return {
      orderlist: [],
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
  mounted() {
    this.getOrderList();
  },
  methods: {
    async getOrderList() {
      //alert('사용자 id에 맞는 주문 내역 가져오기');
      console.log(this.user.id)
      const orders = await axios.get(`http://localhost:8000/order/getorderlist/${this.user.id}`);
      this.orderlist = orders.data;
      console.log('주문 내역들', this.orderlist);
    },
    getStatusMessage(status) {
      switch (status) {
        case 'pending':
          return '주문 접수가 완료되었습니다.';
          case 'delivering':
          return '배달중이에요.';
        case 'delivered':
          return '배달이 완료되었어요.';
        case 'canceled':
          return '주문이 취소되었습니다.';
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
    }
  }
}
</script>

<style>

</style>