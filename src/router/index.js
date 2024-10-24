import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginPage from '../views/LoginPage.vue'
import SignupPage from '../views/SignupPage.vue'
import UserProfilePage from '../views/UserProfilePage.vue'
import StoreRegistration from '../views/StoreRegistration.vue'

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
    path: '/storeregistration',
    name: 'storeregistration',
    component: StoreRegistration
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
