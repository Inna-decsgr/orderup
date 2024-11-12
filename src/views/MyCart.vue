<template>
  <div>
    내 장바구니  
    <div v-if="menucart.length === 0">
      <p>장바구니가 텅 비었어요</p>
      <button>+더 담으러 가기</button>
    </div>
    <div v-else>
      <div v-for="(item, index) in menucart" :key="index" class="menu-item">
        <strong>{{ item.menu ? item.menu.name : item.name}}</strong>
        <p>가격: {{ item.menu ? item.menu.price.toLocaleString() : item.price.toLocaleString() }}원</p>

        <!-- menu가 정의되어 있을 경우 옵션들을 렌더링 -->
        <div v-if="item.menu && item.menu.option_groups && item.menu.option_groups.length > 0">
          <ul>
            <span v-for="(group, groupIndex) in item.menu.option_groups" :key="groupIndex">
              <p v-for="(option, optionIndex) in group.items" :key="optionIndex">
                {{ option.name }} (+{{ option.price.toLocaleString() }}원)
              </p>
            </span>
          </ul>
        </div>

        <!-- menu가 없을 경우 options에서 처리 -->
        <div v-else-if="item.options && Object.keys(item.options).length > 0">
          <ul>
            <li v-for="(price, optionName) in item.options" :key="optionName">
              {{ optionName }} (+{{ price.toLocaleString() }}원)
            </li>
          </ul>
        </div>
      </div>
      <button @click="removemenu">삭제</button>
      <button>{{ totalCartPrice }} - 주문하러 가기</button>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    menucart() {
      return this.$store.state.menucart;
    },
    totalCartPrice() {
      return this.menucart.reduce((total, item) => {
        let itemTotalPrice = item.menu ? item.menu.price : item.price; // 메뉴의 기본 가격 설정

        // 메뉴가 있고 옵션 그룹이 있을 경우 옵션 가격 추가
        if (item.menu && item.menu.option_groups) {
          item.menu.option_groups.forEach(group => {
            group.items.forEach(option => {
              // 선택된 옵션이 있는 경우 해당 가격 추가
              if (item.options && item.options[option.name]) {
                itemTotalPrice += item.options[option.name];
              }
            });
          });
        }

        // 각 항목의 총 가격을 누적해서 합산
        return total + itemTotalPrice;
      }, 0).toLocaleString();
    },
  },
  methods: {
    removemenu() {
      this.$store.commit('clearMenucart');
    }
  }
}
</script>