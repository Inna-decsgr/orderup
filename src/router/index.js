import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginPage from '../views/LoginPage.vue'
import SignupPage from '../views/SignupPage.vue'
import UserProfilePage from '../views/UserProfilePage.vue'
import MyStore from '../views/MyStore.vue'
import StoreRegistration from '../views/StoreRegistration.vue'
import MyMenu from '../views/MyMenu.vue'
import SearchResult from '../views/SearchResult.vue'
import DetailStore from '../views/DetailStore.vue'
import MyCart from '../views/MyCart.vue'
import OrderList from '../views/OrderList.vue'


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
    path: '/userprofile',
    name: 'userprofile',
    component: UserProfilePage
  },
  {
    path: '/mystore',
    name: 'mystore',
    component: MyStore
  },
  {
    path: '/registrationstore',
    name: 'registrationstore',
    component: StoreRegistration
  },
  {
    path: '/mymenu',
    name: 'mymenu',
    component: MyMenu
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
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
