import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store.js'
import axios from 'axios';

axios.defaults.withCredentials = true;  // Axios 요청에서 쿠키를 포함하도록 자격 증명 활성화

// Bootstrap CSS
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import './index.css'

createApp(App)
  .use(router)
  .use(store)
  .mount('#app')
