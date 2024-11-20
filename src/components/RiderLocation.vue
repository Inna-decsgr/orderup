<template>
  <div class="popup-content">
    라이더 배달 현황
    <button @click="handleCancel">x</button>
    <div>
      <div id="map" style="width:100%; height:500px"></div>
    </div>
  </div>
</template>

<script>

export default {
  data() {
    return {
      map: null,
      isMapLoaded: false
    }
  },
  props: {
    cancel: {
      type: Function,
      required: true
    },
    orderid: {
      type: Number,
      required: true
    }
  },
  mounted() {
    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=${process.env.VUE_APP_GOOGLE_MAPS_API_KEY}&callback=initMap&v=weekly&libraries=marker&language=ko&region=KR`;
    script.async = true;
    script.defer = true;

    script.onload = () => {
      this.initMap()
    }
    document.head.appendChild(script);

    window.initMap = this.initMap.bind(this);
  },
  methods: {
    handleCancel() {
      this.cancel(this.orderid)
    },

    async initMap() {
      // Google Maps API가 로드되면 호출되는 초기화 함수
      const position = { lat: 37.5665, lng: 126.9780 };

      // Maps와 Marker 라이브러리 불러오기
      // eslint-disable-next-line
      const { Map } = await google.maps.importLibrary("maps");
      // eslint-disable-next-line
      const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

      // 구글 맵 API에서 필요한 요소 불러와서 지도 객체 생성
      this.map = new Map(document.getElementById("map"), {
        zoom: 18,
        center: position,
        mapId: process.env.VUE_APP_GOOGLE_MAPS_MAP_ID
      });
      console.log(this.map);

      // 마커 추가
      // eslint-disable-next-line
      const marker = new AdvancedMarkerElement({
        map: this.map,
        position: position,
        style: {
          icon: {
      // eslint-disable-next-line
            path: google.maps.SymbolPath.CIRCLE,
      fillColor: "red",
      fillOpacity: 1,
      strokeColor: "white",
      strokeWeight: 2,
      scale: 8
          }
        }
      });
      console.log('마커', marker);
    }
  }
}
</script>



<style>
.popup-content {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  width: 80%;
  max-width: 500px;
}
</style>