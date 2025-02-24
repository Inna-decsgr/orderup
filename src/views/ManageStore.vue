<template>
  <div>
    <p class="font-bold text-lg my-3">가게 관리하기</p>
    <div class="flex justify-between items-center">
      <p><strong>{{ store.name }}</strong></p>
      <button @click="confirmDelete(store.id)" class="bg-violet-500 py-1 px-2 text-white rounded-md text-sm">운영 종료</button>
    </div>
    <div v-if="deletestore" class="border p-3 text-center w-[400px] mx-auto rounded-sm">
      <p class="font-bold">정말로 가게 운영을 종료하시겠습니까?</p>
      <p class="font-bold">종료하시면 가게가 폐점 처리됩니다.</p>
      <button @click="deleteStore(store.id)" class="mt-3 bg-violet-500 text-white text-sm py-1 px-2 rounded-md mr-2">확인</button>
      <button @click="cancelstore" class="bg-violet-500 text-white text-sm py-1 px-2 rounded-md">취소</button>
    </div>
    <div v-if="!deletestore" class="text-sm my-4">
      <button @click="editMode" class="p-2 border-b-[2px] mr-3" :class="{'font-bold border-black' : editmode}">가게 정보 수정</button>
      <button @click="gotoMenu({id: store.id, name: store.name})" class="p-2 border-b-[2px] mr-3" :class="{'font-bold border-black' : showmenu}">메뉴 관리</button>
      <button @click="gotoReview" class="p-2 border-b-[2px] mr-3" :class="{'font-bold border-black' : showreview}">리뷰 관리</button>
      <div class="inline-block">
        <button @click="showNewOrder" class="p-2 border-b-[2px] mr-3" :class="{'font-bold border-black' : showorder}">주문 관리</button>
        <span v-if="ordercount[store.id] !== undefined && ordercount[store.id]" class="pl-2">{{ ordercount[store.id] }}</span>
      </div>
    </div>
    <div v-if="editmode">
      <EditStore :store="store" :cancel="handleCancel" />
    </div>
    <div v-if="showmenu">
      <MyMenu :store="store" :cancel="handleCancel" />
    </div>
    <div v-if="showreview">
      <ManageReview :storeid="store.id"/>
    </div>
    <div v-if="showorder">
      <ManageOrder :storeid="store.id" :cancel="handleCancel" />
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import EditStore from '../components/EditStore.vue';
import MyMenu from '../components/MyMenu.vue';
import ManageOrder from '../components/ManageOrder.vue';
import ManageReview from '../components/ManageReview.vue';
import { mapGetters } from 'vuex';

export default {
  components: {
    EditStore,
    MyMenu,
    ManageOrder,
    ManageReview
  },
  data() {
    return {
      index: null,
      editmode: false,
      showmenu: false,
      showorder: false,
      showreview: false,
      ordercount: {},
      deletestore: false
    };
  },
  mounted() {
    console.log('Store from Vuex', this.store);
    this.getOrderLength();
  },
  computed: {
    ...mapGetters(['getUser', 'getStore']),
    user() {
      return this.getUser
    },
    store() {
      return this.getStore || {}
    }
  },
  methods: {
    editMode() {
      this.editmode = true;
      this.resetModes('edit');
    },
    handleCancel() {
      this.editmode = false;
      this.showmenu = false;
      this.showorder = false;
    },
    confirmDelete() {
      this.deletestore = true;
    },
    async getOrderLength() {
      try {
        const response = await axios.get(`http://localhost:8000/order/orderlength/${this.store.id}`);
        this.ordercount[this.store.id] = response.data.order_count;
      } catch (error) {
        console.error('주문 갯수 가져오기 실패:', error)
      }
    },
    async deleteStore(storeid) {
      // 가게 삭제 로직 구현
      console.log(storeid);
      const csrfResponse = await axios.get("http://localhost:8000/order/csrftoken/");
      const csrfToken = csrfResponse.data.csrfToken;

      const response = await axios.delete(`http://localhost:8000/order/deletestore/${storeid}/`, {
        headers: {
          'X-CSRFToken': csrfToken,
        }
      });
      console.log(response.data);
      alert('가게가 성공적으로 삭제되었습니다.');
      this.getMyStore();
    },
    gotoMenu() {
      this.showmenu = true;
      this.resetModes('menu');
    },
    showNewOrder() {
      this.showorder = true;
      this.resetModes('order');
    },
    gotoReview() {
      this.showreview = true;
      this.resetModes('review');
    },
    resetModes(activeComponent) {
      if (activeComponent !== 'edit') {
        this.editmode = false;
      }
      if (activeComponent !== 'menu') {
        this.showmenu = false;
      }
      if (activeComponent !== 'order') {
        this.showorder = false;
      }
      if (activeComponent !== 'review') {
        this.showreview = false;
      }
    },
    cancelstore() {
      this.deletestore = false;
    }
  }
}
</script>