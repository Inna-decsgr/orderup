<template>
  <div>
    <div class="flex justify-between items-center pt-3 px-3">
      <p v-if="user"><i class="fa fa-map-marker"></i> <strong>{{ this.user.address }}</strong></p>
      <div class="flex items-center ml-auto">
        <button type="button" class="btn btn-light text-xs" v-if="!isLoggedIn" @click="gotoLogin">로그인</button>
        <button v-if="user && user.is_owner" @click="gotoMyStore" class="mr-5">
          <i class="fa-solid fa-store"></i>
        </button>
        <button v-if="user" @click="gotoMyCart" class="mr-2">
          <i class="fa-solid fa-cart-shopping"></i>
        </button>
      </div>
    </div>
    <div class="px-3">
      <SearchBar />
    </div>
    <div>
      <div class="mt-4 py-4 rounded-t-md" style="box-shadow: 0 -4px 6px rgba(0, 0, 0, 0.15);">
        <div class="text-center w-[400px] h-[180px] mx-auto">
          <div class="food_category">
            <button class="category-btn" @click="gotofilteredStore(categories[0])">
              <span>🍔</span>
              <p>패스트푸드</p>
            </button>
            <button class="category-btn" @click="gotofilteredStore(categories[1])">
              <span>🍜</span>
              <p>중식</p>
            </button>
            <button class="category-btn" @click="gotofilteredStore(categories[2])">
              <span>🌭</span><br/>
              <p class="inline-block">분식</p>
            </button>
            <button class="category-btn" @click="gotofilteredStore(categories[3])">
              <span>🍣</span>
              <p>일식</p>
            </button>
            <button class="category-btn" @click="gotofilteredStore(categories[4])">
              <span>🧁</span>
              <p>카페·디저트</p>
            </button>
          </div>
          <div class="food_category">
            <button class="category-btn" @click="gotofilteredStore(categories[5])">
              <span>🍱</span>
              <p>아시안</p>
            </button>
            <button class="category-btn" @click="gotofilteredStore(categories[6])">
              <span>🍝</span>
              <p>양식</p>
            </button>
            <button class="category-btn" @click="gotofilteredStore(categories[7])">
              <span>🍕</span>
              <p>피자</p>
            </button>
            <button class="category-btn" @click="gotofilteredStore(categories[8])">
              <span>🥩</span>
              <p>족발·보쌈</p>
            </button>
            <button class="category-btn" @click="gotofilteredStore(categories[9])">
              <span>🍲</span>
              <p>찜·탕</p>
            </button>
          </div>
        </div>
        <div class="flex">
          <button class="font-bold text-[14px] mx-auto border-t-[1px] border-b-[1px] w-full mt-[30px] py-2" @click="gotofilteredStore">
            음식배달에서 더보기
            <i class="fa-solid fa-chevron-right"></i>
          </button>
        </div>
      </div>
      <div v-if="user && user.id">
        <RecentOrderStore />
      </div>
      <div style="margin-top: 50px; margin-bottom: 50px;">
        <SaleBanner />
      </div>
      <div v-if="!showfilteredstore">
        <OrderChart />
      </div>
      <div>
        <BottomBanner />
      </div>
    </div>
  </div>
</template>

<script>
import SearchBar from '../components/SearchBar.vue'
import OrderChart from '../components/OrderChart.vue'
import RecentOrderStore from '../components/RecentOrderStore.vue'
import SaleBanner from '../components/SaleBanner.vue'
import BottomBanner from '../components/BottomBanner.vue'
import { mapGetters } from 'vuex';



export default {
  components: {
    SearchBar,
    OrderChart,
    RecentOrderStore,
    SaleBanner,
    BottomBanner
  },
  computed: {
    ...mapGetters(['isLoggedIn', 'getUser']),
    user() {
      return this.$store.getters.getUser;
    }
  },
  data() {
    return {
      categories: [
        { id: 1, name: '패스트푸드' },
        { id: 2, name: '중식' },
        { id: 3, name: '분식' },
        { id: 4, name: '일식' },
        { id: 5, name: '카페·디저트' },
        { id: 6, name: '아시안' },
        { id: 7, name: '양식' },
        { id: 8, name: '피자' },
        { id: 9, name: '족발·보쌈' },
        { id: 10, name: '찜·탕'}
      ],
      showfilteredstore:false
    }
  },
  methods: {
    categoryStore(categoryid) {
      // 카테고리 ID에 맞는 가게 데이터 필터링하기
      this.filteredData = this.storeData.filter((store) => store.categories.some((category) => category === categoryid.name));
      this.showfilteredstore = true
    },
    gotoLogin() {
      this.$router.push('/login');
    },
    gotoMyCart() {
      this.$router.push('/mycart')
    },
    gotoMyStore() {
      this.$router.push('/mystore');
    },
    gotofilteredStore(categoryid) {
      this.$router.push({
        path: '/filteredstore',
        query: {
          category: categoryid.name
        }
      })
    }
  }
}
</script>

<style>
.category-btn {
  height: 90px;
  width: 80px;
  font-size: 11px;
  text-align: center;
}

.food_category span {
  background: rgb(240, 239, 239);
  border-radius: 25px;
  font-size: 35px;
  padding: 10px;
  width: 70px;
  height: 70px;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  line-height: 1;
}

.food_category p {
  font-weight: bold;
  margin-top: 3px;
  font-size: 11px;
}

.food_category:last-child {
  margin-top: 15px;
}


</style>