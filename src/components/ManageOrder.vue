<template>
  <div>
    <div v-if="orders">
      <div v-for="order in orders" :key="order.order_id">
        <div v-for="orderitem in order" :key="orderitem.order_id">
          <div v-if="getStatusMessage(orderitem.status) === '새로운 주문'" class="flex justify-between items-center bg-black text-white p-3">
            <p class="text-xl font-bold">{{  convertToKST(orderitem.ordered_at)}} 결제완료</p>
            <div>
              <button v-if="orderitem.status === 'pending'" @click="handleOrder(orderitem.order_id, 'accept')" class="bg-blue-500 font-bold text-white py-2 px-4 rounded-[18px] mr-3 hover:bg-blue-600">접수</button>
              <button v-if="orderitem.status === 'pending'" @click="handleOrder(orderitem.order_id, 'reject')" class="bg-blue-500 font-bold text-white py-2 px-4 rounded-[18px] hover:bg-blue-600">거절</button>
            </div>
          </div>
          <div v-if="orderitem.status === 'accepted'" class="flex justify-between items-center bg-black text-white p-3">
            <p class="font-bold text-lg">음식 조리 중</p>
            <button v-if="iscooking === false" @click="setcooked" class="bg-blue-500 font-bold text-white py-2 px-4 rounded-[18px] mr-3 hover:bg-blue-600">
            조리 완료
            </button>
            <button v-if="iscooking === true" @click="gotoSelectRider({ order_id: orderitem.order_id, status: orderitem.status })" class="bg-blue-500 font-bold text-white py-2 px-4 rounded-[18px] mr-3 hover:bg-blue-600">
            라이더 배정
            </button>
          </div>
          <div v-if="orderitem.status === 'canceled'" class="flex justify-between items-center bg-black text-white p-3">
            <p class="font-bold text-lg">주문 취소됨</p>
          </div>
          <div v-if="orderitem.status === 'delivering'" class="flex justify-between items-center bg-black text-white p-3">
            <p class="font-bold text-lg">라이더가 배달중입니다💨</p>
            <button @click="setdelivered(orderitem.order_id)" class="bg-blue-500 font-bold text-white py-2 px-4 rounded-[18px] mr-3 hover:bg-blue-600">
            배달 완료 처리
            </button>
          </div>
          <div v-if="orderitem.status === 'delivered'" class="flex justify-between items-center bg-black text-white p-3">
            <p class="font-bold text-lg">라이더가 배달을 완료했습니다🛵</p>
            <button class="bg-blue-500 font-bold text-white py-2 px-4 rounded-[18px] mr-3 hover:bg-blue-600">
            배달 완료
            </button>
          </div>
          <div v-if="orderitem.status === 'rejected'" class="flex justify-between items-center bg-black text-white p-3">
            <p class="font-bold text-lg">주문 거절됨</p>
          </div>
          <div class="m-3 bg-white">
            <p class="font-bold text-lg mb-2 border-b pb-2">주문정보</p>
            <p><span class="font-bold">주문 번호</span> {{ generatecode(Number(orderitem.order_id)) }}</p>
            <p><span class="font-bold">주문 상태</span> {{ getStatusMessage(orderitem.status) }}</p>
            <p><span class="font-bold">주문 일시</span> {{ formattedDate(orderitem.ordered_at) }}</p>
            <p><strong>주소</strong> : {{ orderitem.user_address }}</p>
            <p class="mb-3"><span class="font-bold">주문자 전화번호</span> {{ orderitem.user_phone }}</p>
            <p class="font-bold pb-2 border-b mb-2">주문 상품</p>
            <div class="border-b pb-3 mb-3">
              <div class="flex justify-between items-center border-b pb-2 mb-2 font-bold text-gray-400">
                <span>상품</span>
                <span class="pl-[180px]">수량</span>
                <span>금액</span>
              </div>
              <ul v-for="menu in orderitem.order_items" :key="menu.item">
                <li class="flex justify-between items-center font-bold relative">
                  <p>{{ menu.item }}</p>
                  <p class="absolute right-[175px]">1</p>
                  <p>{{ menu.price.toLocaleString() }}원</p>
                </li>
                <div v-if="menu.options && menu.options.length > 0">
                  <li v-for="option in menu.options" :key="option.name" class="flex justify-between items-center font-bold text-gray-400 text-[15px]">
                    <p><span>ㄴ</span>{{ option.name }}</p>
                    <p class="pl-[170px]">1</p>
                    <p>{{ option.price.toLocaleString() }}원 </p>
                  </li>
                </div>
              </ul>
            </div>
            <div class="flex justify-between items-center font-bold">
              <p>상품합계</p>
              <p>{{ Number(orderitem.total_price).toLocaleString() }}원</p>
            </div>
            <div v-if="orderitem.user_coupon_id" class="flex justify-between items-center font-bold">
              <p>쿠폰 적용</p>
              <p>- {{ Number(orderitem.discount_amount).toLocaleString() }}원</p>
            </div>
            <div class="flex justify-between items-center font-bold border-b pb-3 mb-3">
              <p>배달비</p>
              <p>+ {{ orderitem.delivery_fee }}원</p>
            </div>
            <div class="flex justify-between items-center font-bold border-b pb-3 mb-3">
              <p>총 결제금액</p>
              <p>{{ orderitem.user_coupon_id ? (Number(orderitem.total_price) + Number(orderitem.delivery_fee) - Number(orderitem.discount_amount)).toLocaleString() : Number(orderitem.total_price).toLocaleString() }}원</p>
            </div>
            <div class="flex justify-between items-center font-bold">
              <p>결제 방식</p>
              <p>{{ orderitem.payment_method }}</p>
            </div>
          </div>
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
      orders: [],
      iscooking: false,
      message: null
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
    },
    convertToKST(time) {
      const utcDate = new Date(time);

      // 한국 시간으로 변환
      const options = { hour: '2-digit', minute: '2-digit', hour12: false, timeZone: 'Asia/Seoul' };
      const kstTime = utcDate.toLocaleTimeString('ko-KR', options);

      return kstTime;
    },
    generatecode(number) {
      // 공통된 문자열을 기반으로 랜덤한 코드 리스트 생성
      const prefix = 'WEKRIUV'

      // 한 자리 숫자일 경우 앞에 0을 붙이기
      const formattedNumber = String(number).padStart(2, '0');

      // 최종 코드 생성
      const unique_code = prefix + formattedNumber

      return unique_code
    },
    setcooked() {
      this.iscooking = true
    },
    async setdelivered(orderid) {
      const confirmed = confirm('배달 완료 처리하시겠습니까?');

      if (confirmed) {
        try {
          const csrfResponse = await axios.get("http://localhost:8000/order/csrftoken/");
          const csrfToken = csrfResponse.data.csrfToken;

          const response = await axios.put(`http://localhost:8000/order/completedelivery/${orderid}/`, null, {
            headers: {
              'X-CSRFToken': csrfToken,
            }
          });
          console.log('배달 완료 처리', response.data);
          this.message = response.data.message
        } catch (error) {
          console.error('배달 완료 처리 중 오류 발생:', error);
          alert('배달 완료 처리에 실패했습니다.');
        }
      }
    }
  }
}
</script>