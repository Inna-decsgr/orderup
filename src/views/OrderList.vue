<template>
  <div>
    <div v-if="orderlist.length > 0">
      <h3><strong>주문 내역</strong></h3>
      <div v-for="order in orderlist" :key="order.order_id">
        <div>
          <p>{{ getStatusMessage(order.status) }}</p>
          <p v-if="order.status === 'accepted'">
            <i class="fa-solid fa-fire-burner"></i>
            음식을 맛있게 조리하고 있습니다
          </p>
          <button v-if="order.status === 'delivering'" @click="showLocation(order.order_id)">배달 현황보기</button>
          <div v-if="showDelivering[order.order_id]" class="popup">
            <RiderLocation :cancel="closepopup" :orderid="order.order_id" ref="RiderLocationComponent" />
          </div>
          <button v-if="order.status === 'pending'" @click="cancelorder(order.order_id)">주문 취소</button>
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
            <p>주문 금액 {{ order.total_price.toLocaleString() }}원</p>
            <p>총 결제 금액 <strong>{{ (order.total_price).toLocaleString() }}원</strong></p>
            <p>결제방법 {{ order.payment_method }}</p>
          </div>
        </div>
        <hr />
      </div>
    </div>
    <div v-else>
      <p>주문 내역이 없습니다.</p>
      <button @click="gotoHome">주문하러 가기</button>
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
      this.orderlist = orders.data;
      console.log('주문 내역들', this.orderlist);
    },
    getStatusMessage(status) {
      switch (status) {
        case 'pending':
          return '주문이 완료되었습니다.';
        case 'accepted':
          return '주문이 수락되었습니다.';
        case 'delivering':
          return '배달원이 음식을 픽업하고 배달중입니다💨';
        case 'delivered':
          return '배달이 완료되었어요.';
        case 'canceled':
          return '주문이 취소되었습니다.';
        case 'rejected':
          return '주문이 거절되었습니다.';
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
    gotoHome() {
      this.$router.push('/')
    },
    showLocation(orderid) {
      this.showDelivering[orderid] = true

      // Vue의 nextTick을 사용해서 렌더링 후 startMoving 호출될 수 있도록
      this.$nextTick(() => {
        const riderLocationComponent = this.$refs.RiderLocationComponent;

        if (riderLocationComponent && typeof riderLocationComponent.startMoving === 'function') {
          riderLocationComponent.startMoving();
        } else {
          console.error('startMoving 메서드가 정의되지 않았습니다.')
        }
      })
    },
    closepopup(orderid) {
      this.showDelivering[orderid] = false
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
</style>