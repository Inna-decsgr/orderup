import { createStore } from 'vuex';
import createPersistedState from 'vuex-persistedstate';

const store = createStore({
  state() {
    return {
      user: null, // 사용자 정보 저장,
      menucart: [],
      store: [],
      order: []
    };
  },
  mutations: {
    setUser(state, user) {
      state.user = user; // 사용자 정보를 저장하는 mutation
    },
    clearUser(state) {
      state.user = null;  // 사용자 정보를 초기화하는 mutation
    },
    setMenucart(state, cart) {
      state.menucart = cart;
    },
    clearMenucart(state) {
      state.menucart = []; // 장바구니 정보 초기화하는 mutation
    },
    setStore(state, store) {
      state.store = store;
    },
    setOrder(state, order) {
      state.order = order;
    }
  },
  actions: {
    login({ commit }, user) {
      commit('setUser', user); // 사용자 정보를 저장하는 mutation 호출
    },
    logout({ commit }) {
      commit('clearUser');
    }
  },
  getters: {
    isLoggedIn(state) {
      return !!state.user; // 사용자가 로그인했는지 확인
    },
    getUser(state) {
      return state.user; // 사용자 정보 가져오기
    },
    getUserId(state) {
      return state.user.id  // 사용자 정보 중 아이디만 가져오기
    },
    getStore(state) {
      return state.store
    },
    getOrder(state) {
      return state.order
    }
  },
  plugins: [createPersistedState()],
});

export default store;
