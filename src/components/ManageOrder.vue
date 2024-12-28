<template>
  <div>
    <p><strong>주문 관리 페이지</strong></p>
    <div v-if="orders">
      <div v-for="order in orders" :key="order.order_id">
        <div v-for="orderitem in order" :key="orderitem.order_id">
          <p><strong>주문 번호</strong> : {{ orderitem.order_id }}</p>
          <p>주문 일시 : {{ formattedDate(orderitem.ordered_at) }}</p>
          <p><strong>주문 상태</strong> : {{ getStatusMessage(orderitem.status) }}</p>
          <p><strong>주소</strong> : {{ orderitem.user_address }}</p>
          <p><strong>주문자 번호</strong> : {{ orderitem.user_phone }}</p>
          <strong>주문 메뉴</strong>
          <ul v-for="menu in orderitem.order_items" :key="menu.item">
            <li>{{ menu.item }} {{ menu.price }}원</li>
            <div v-if="menu.options && menu.options.length > 0">
              <p>(+추가 옵션)</p>
              <li v-for="option in menu.options" :key="option.name">
                {{ option.name }} (+{{ option.price }}원) 
              </li>
            </div>
          </ul>
          <p>총 금액 <strong>{{ Number(orderitem.total_price).toLocaleString() }}원</strong></p>
          <p>배달비 + {{ orderitem.delivery_fee }}원</p>
          <p v-if="orderitem.user_coupon_id">쿠폰 적용 - <span>{{ Number(orderitem.discount_amount).toLocaleString() }}원</span></p>
          <p><strong>결제된 금액: {{ orderitem.user_coupon_id ? (Number(orderitem.total_price) + Number(orderitem.delivery_fee) - Number(orderitem.discount_amount)).toLocaleString() : Number(orderitem.total_price).toLocaleString() }}원</strong></p>
          <p><strong>결제 방식</strong> : {{ orderitem.payment_method }}</p>
          <button v-if="orderitem.status === 'pending'" @click="handleOrder(orderitem.order_id, 'accept')">수락하기</button>
          <button v-if="orderitem.status === 'pending'" @click="handleOrder(orderitem.order_id, 'reject')">거절하기</button>
          <div v-if="orderitem.status === 'accepted'">
            <p>음식 조리 중</p>
            <button @click="gotoSelectRider({ order_id: orderitem.order_id, status: orderitem.status })">
              조리 완료
            </button>
          </div>
          <hr/>
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
import { formatDate } from '../utils/dateutils';

export default {
  props: {
    storeid: {
      type: Number,
      required: true,
    }
  },
  data() {
    return {
      orders: []
    }
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
          return '주문 수락';
        case 'delivering':
          return '배달중';
        case 'delivered':
          return '배달 완료';
        case 'canceled':
          return '주문 취소';
        case 'rejected':
          return '주문 거절';
        default:
          return '상태 정보 없음';
      }
    },
    async handleOrder(orderid, orderType) {
      const isConfirmed = window.confirm(`이 주문을 ${orderType === 'accept' ? '수락' : '거절'}하시겠습니까?`);

      if (isConfirmed) {
        const csrfResponse = await axios.get("http://localhost:8000/order/csrftoken/");
        const csrfToken = csrfResponse.data.csrfToken;
        
        console.log(orderid);
        const response = await axios.put(`http://localhost:8000/order/${orderType}order/${orderid}/`, null, {
          headers: {
            'X-CSRFToken': csrfToken,
          }
        });
        alert(`주문이 ${orderType === 'accept' ? '수락' : '거절'} 되었습니다.`)
        console.log(response.data);
        this.getNewOrder();
      }
    },
    formattedDate(date) {
      return formatDate(date);
    },
    gotoSelectRider(order) {
      this.$router.push({
        path: '/selectrider',
        query: {
          order: JSON.stringify(order)
        }
      })
    }
  }

}
</script>