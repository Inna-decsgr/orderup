<template>
  <div>
    <div class="p-3">
      <div class="flex items-center">
        <i class="fa-solid fa-arrow-left pr-4 cursor-pointer" @click="gotohome"></i>
        <p class="font-bold text-xl">주문 내역</p>
      </div>
      <p class="font-bold mt-3 pl-8">배달·포장</p>
    </div>
    <div v-if="orderlist.length > 0" class="p-3 bg-gray-100">
      <div v-for="order in orderlist" :key="order.order_id" class="p-3 mb-3 bg-white">
        <div>
          <div class="pt-1 pb-2">
            <div class="flex justify-between items-center">
              <div class="font-bold text-gray-400 text-xs">
                <p>{{ formatUtcToKoreanDate(order.ordered_at) }} · {{ getStatusMessage(order.status) }}</p>
              </div>
              <button @click="gotodetailorder(order.order_id)" class="text-xs border py-1 px-2 rounded-xl font-bold">주문상세</button>
            </div>
          </div>
          <div v-if="showDelivering[order.order_id]" class="popup">
            <RiderLocation :cancel="closepopup" :orderid="order.order_id" @confirm="handleConfirm(order.order_id)"/>
          </div>
          <div class="flex items-center pb-3">
            <img :src="order.restaurant.image_url" alt="가게 이미지" class="w-[100px] h-[100px] rounded-[38px] border">
            <div class="pl-3">
              <div class="flex items-center">
                <p class="font-bold text-lg pr-2">{{ order.restaurant.name }}</p>
                <button @click="detailstore({id:order.restaurant.id, name: order.restaurant.name})">
                  <i class="fa-solid fa-chevron-right"></i>
                </button>
              </div>
              <div class="font-bold flex">
                <p v-if="order.items.length > 0" class="pr-2 text-sm">
                  {{ order.items[0].menu.name }} {{ order.items.length > 1 ? `외 ${order.items.length - 1}개` : `${order.items[0].quantity}개` }}
                </p>
                <p class="text-sm">
                  {{ (Number(order.total_price) + Number(order.restaurant.deliveryfee)
                  - Number(order.discount_amount)).toLocaleString() }}원
                </p>
              </div>
              <p v-if="order.discount_amount > 0" class="border-1 border-violet-500 w-[90px] text-center text-xs py-[5px] px-[8px] font-bold rounded-2xl mt-1"><span class="text-violet-700">{{ Number(order.discount_amount).toLocaleString()}}원</span> 할인</p>
              <p v-if="order.review === true" class="border-1 border-violet-500 w-[110px] text-center text-xs py-[5px] px-[8px] font-bold rounded-2xl">후기 작성완료</p>
            </div>
          </div>
          <button v-if="order.status === 'delivered' && order.review === false" @click="gotoReview(order)" class="font-bold border-1 border-violet-700 rounded-sm text-violet-700 w-full py-2">
            리뷰쓰기
          </button>
          <button v-if="order.status === 'delivered' && order.review === true" @click="gotoMyReview(order.restaurant)" class="font-bold border-1 border-violet-700 rounded-sm text-violet-700 w-full py-2">
            리뷰 보러가기
          </button>
          <button v-if="order.status === 'pending'" @click="cancelorder(order.order_id)" class="font-bold border-1 border-violet-700 rounded-sm text-violet-700 w-full py-2">
            주문 취소
          </button>
          <button v-if="order.status === 'delivering'" @click="showLocation(order.order_id)" class="font-bold border-1 border-violet-700 rounded-sm text-violet-700 w-full py-2">
            배달 현황 보기
          </button>
        </div>
      </div>
    </div>
    <div v-else class="text-center pt-[100px] px-[60px]">
      <p class="font-bold">주문 내역이 없어요.</p>
      <p class="text-gray-500 text-sm pt-2">비회원 주문내역은 30일동안 확인 가능합니다. 오더업 회원 탈퇴하시면 비회원 주문내역을 확인할 수 있습니다.</p>
      <button @click="gotofilteredStore" class="bg-violet-400 w-[200px] p-2 text-white text-sm font-bold my-5 rounded-md">주문하러 가기</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import {reactive} from 'vue'
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
          return '주문완료';
        case 'accepted':
          return '주문수락';
        case 'delivering':
          return '배달중';
        case 'delivered':
          return '배달완료';
        case 'canceled':
          return '주문취소';
        case 'rejected':
          return '주문거절';
        default:
          return '상태 정보 없음';
      }
    },
    generateOrderId(orderid) {
      // 주문 아이디를 12자리로 포맷, 앞에 0을 채우고 접두사 'T1VI' 추가
      const paddedId = orderid.toString().padStart(8, '0'); // 숫자를 문자열로 바꾸고 12자리로 패딩
      return `T1VI${paddedId}`;
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
    },
    formatUtcToKoreanDate(time) {
      // UTC 시간을 Date 객체로 변환
      const utcDate = new Date(time);

      // 한국 시간(KST, UTC+9)으로 변환
      const kstDate = new Date(utcDate.getTime() + 9 * 60 * 60 * 1000);

      // 날짜 포맷 (월.일)
      let monthDay = kstDate.toLocaleDateString('ko-KR', { month: 'numeric', day: 'numeric' });

       // 혹시라도 점(.)이 포함되었으면 제거
      monthDay = monthDay.replace(/\.$/, '');

      // 요일 가져오기 (토, 일, 월...)
      const weekday = kstDate.toLocaleDateString('ko-KR', { weekday: 'short' });

      return `${monthDay} (${weekday})`;
    },
    detailstore(store) {
      this.$router.push('/detailstore'),
      this.$store.commit('setStore', store);
    },
    gotodetailorder(orderid) {
      this.$router.push({
        name: 'DetailOrder',
        params: {
          orderid: orderid,
        }
      });
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