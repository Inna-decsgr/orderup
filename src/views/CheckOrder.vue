<template>
  <div>
    <h3>주문 확인서</h3>
    <strong>[{{ store }}]</strong>
    <div v-for="(item, index) in menucart" :key="index" class="menu-item">
      <strong>{{ item.menu ? item.menu.name : item.name}}</strong>
      <p>가격: {{ item.menu ? item.menu.price.toLocaleString() : item.price.toLocaleString() }}원</p>

      <!--옵션 그룹이 있는 경우 옵션 출력-->
      <div v-if="item.menu && Array.isArray(item.menu.option_groups) && item.menu.option_groups.length > 0">
        <ul>
          <span v-for="(group, groupIndex) in item.menu.option_groups" :key="groupIndex">
            <p v-for="(option, optionIndex) in group.items" :key="optionIndex">
              {{ option.name }} (+{{ option.price.toLocaleString() }}원)
            </p>
          </span>
        </ul>
      </div>

      <p>
        {{ 
          item.menu 
          ? ( 
            item.menu.price + (item.menu.option_groups ? item.menu.option_groups.reduce((acc, group) => {return acc + group.items.reduce((groupAcc, option) => { return groupAcc + (item.options && item.options[option.name] ? item.options[option.name] : 0);
            }, 0);
          }, 0)
          : 0)) : item.price
        }}
      </p>
    </div>
    

    <!--주문 총 금액-->
    <button @click="ordermenu(menucart)">{{ totalCartPrice }}원 - 배달 주문하기</button>
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
    store() {
      return this.$route.query.store
    }
  },
  methods: {
    ordermenu(menucart) {
      alert('메뉴 주문')
      console.log('주문할 메뉴', menucart)
    }
  }
}
</script>

<style>
ul {
  list-style: none;
  padding-left: 0 !important;
  margin: 0;
}
</style>