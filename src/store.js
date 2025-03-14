import { createStore } from 'vuex';
import createPersistedState from 'vuex-persistedstate';

const store = createStore({
  state() {
    return {
      user: null, // 사용자 정보 저장,
      menucart: [],
      store: [],
      order: [],
      likedstore: [],
      category: '',
      searchKeywords: []
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
    },
    setLikedStores(state, likedStores) {
      state.likedstore = likedStores;
    },
    addStoreToLiked(state, storeid) {
      if (!state.likedstore.includes(storeid)) {
        state.likedstore.push(storeid);
      }
    },
    removeStoreFromLiked(state, storeid) {
      state.likedstore = state.likedstore.filter(id => id !== storeid);
    },
    setCategory(state, category) {
      state.category = category
    },
    removeMenuItem(state, id) {
      state.menucart = state.menucart.filter((item) => item.id !== id)
    },
    setSearchKeyword(state, keyword) {  // 최근 검색 기록에 해당 키워드 추가
      // 중복 키워드를 방지
      if (state.searchKeywords.includes(keyword)) {
        state.searchKeywords = state.searchKeywords.filter(k => k !== keyword);
      }

      // 새로운 검색 키워드 맨 앞에 추가하기
      state.searchKeywords.unshift(keyword);

      // 최대 5개로 제한
      if (state.searchKeywords.length > 5) {
        state.searchKeywords.pop(); // 배열 맨 마지막 요소 제거
      }
    },
    removekeyword(state, keyword) {  // 최근 검색 기록에서 해당 키워드 삭제
      state.searchKeywords = state.searchKeywords.filter(k => k !== keyword);
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
    },
    getLikedStore(state) {
      return state.likedstore
    },
    getCategory(state) {
      return state.category
    },
    getMenuCart(state) {
      return state.menucart
    },
    getSearchKeywords(state) {
      return state.searchKeywords
    }
  },
  plugins: [createPersistedState()],
});

export default store;
