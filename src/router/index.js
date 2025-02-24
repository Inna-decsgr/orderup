import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginPage from '../views/LoginPage.vue'
import SignupPage from '../views/SignupPage.vue'
import UserProfilePage from '../components/UserProfilePage.vue'
import MyStore from '../views/MyStore.vue'
import StoreRegistration from '../views/StoreRegistration.vue'
import SearchResult from '../views/SearchResult.vue'
import DetailStore from '../views/DetailStore.vue'
import MyCart from '../views/MyCart.vue'
import OrderList from '../views/OrderList.vue'
import SelectRider from '../views/SelectRider.vue'
import RegisterReview from '../views/RegisterReview.vue'
import ManageStore from '../views/ManageStore.vue'
import MyReview from '../views/MyReview.vue'
import UserStoreLike from '../views/UserStoreLike.vue'
import MyOrderup from '../views/MyOrderup.vue'
import FilteredStore from '../views/FilteredStore.vue'
import AllMyReviews from '../views/AllMyReviews.vue'
import AllMyCoupons from '../views/AllMyCoupons.vue'
import AllMyStores from '../views/AllMyStores.vue'


const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginPage
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignupPage
  },
  {
    path: '/myorderup/editprofile',
    name: 'edituserprofile',
    component: UserProfilePage
  },
  {
    path: '/mystore',
    name: 'mystore',
    component: MyStore,
    children: [
      {
        path: 'allmystores',
        name: 'allmystores',
        component: AllMyStores
      },
      {
        path: '/registrationstore',
        name: 'registrationstore',
        component: StoreRegistration
      },
      {
        path: '/allmyreviews',
        name: 'AllMyReviews',
        component: AllMyReviews
      },
        {
        path: '/manageStore',
        name: 'ManageStore',
        component: ManageStore
      },
    ]
  },
  {
    path: '/searchresult',
    name: 'searchresult',
    component: SearchResult
  },
  {
    path: '/detailstore',
    name: 'detailstore',
    component: DetailStore
  },
  {
    path: '/mycart',
    name: 'mycart',
    component: MyCart
  },
  {
    path: '/orderlist',
    name: 'orderlist',
    component: OrderList
  },
  {
    path: '/selectrider',
    name: 'selectrider',
    component: SelectRider
  },
  {
    path: '/newreview',
    name: 'newreview',
    component: RegisterReview
  },
  {
    path: '/myreview',
    name: 'MyReview',
    component: MyReview
  },
  {
    path: '/userlike',
    name: 'UserStoreLike',
    component: UserStoreLike
  },
  {
    path: '/myorderup',
    name: 'MyOrderup',
    component: MyOrderup
  },
  {
    path: '/filteredstore',
    name: 'FilteredStore',
    component: FilteredStore
  },
  {
    path: '/allmycoupons',
    name: 'AllMyCoupons',
    component: AllMyCoupons
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
