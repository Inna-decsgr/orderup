<template>
  <div>
    <p><strong>주문 관리 페이지</strong></p>
    <div v-if="orders">
      <div v-for="order in orders" :key="order.order_id">
        <div v-for="orderitem in order" :key="orderitem.order_id">
          <p><strong>주문 번호</strong> : {{ orderitem.order_id }}</p>
          <p><strong>주문 상태</strong> : {{ getStatusMessage(orderitem.status) }}</p>
          <p><strong>주소</strong> : {{ orderitem.user_address }}</p>
          <p><strong>주문자 번호</strong> : {{ orderitem.user_phone }}</p>
          <strong>주문된 메뉴</strong>
          <ul v-for="menu in orderitem.order_items" :key="menu.item">
            <li>{{ menu.item }} {{ menu.price }}원</li>
            <div v-if="menu.options && menu.options.length > 0">
              <p>(+추가 옵션)</p>
              <li v-for="option in menu.options" :key="option.name">
                {{ option.name }} (+{{ option.price }}원) 
              </li>
            </div>
          </ul>
          <p><strong>결제된 금액: {{ Number(orderitem.total_price).toLocaleString() }}원</strong></p>
          <p><strong>결제 방식</strong> : {{ orderitem.payment_method }}</p>
          <button v-if="orderitem.status === 'pending'">주문 접수하기</button>
        </div>
      </div>
    </div>
    <div v-else>
      <p>새로 들어온 주문이 없습니다.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      orders: []
    }
  },
  computed: {
    storeid() {
      return this.$route.query.storeid;
    },
  }, 
  mounted() {
    this.getNewOrder();
  },
  methods: {
    async getNewOrder() {
      console.log('새로 들어온 주문 가져오기')
      const response = await axios.get(`http://localhost:8000/order/getneworder/${this.storeid}`);
      this.orders = response.data;
      console.log(this.orders);
    },
    getStatusMessage(status) {
      switch (status) {
        case 'pending':
          return '새로운 주문';
        case 'accepted':
          return '주문 접수';
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
  }

}
</script>