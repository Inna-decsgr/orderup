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
      marker: null,
      positions: [
        { lat: 37.5665, lng: 126.9780 }, // 음식점
        { lat: 37.5700, lng: 126.9850 }, // 고객 1
        { lat: 37.5800, lng: 127.0000 }, // 고객 2
      ],
      currentIndex: 0,  // 현재 위치 인덱스
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
    if (!document.getElementById('google-maps-script')) {
      const script = document.createElement('script');
      script.id = 'google-maps-script';
      script.src = `https://maps.googleapis.com/maps/api/js?key=${process.env.VUE_APP_GOOGLE_MAPS_API_KEY}&callback=initMap&libraries=places&language=ko&region=KR`;
      script.async = true;
      script.defer = true;

      script.onload = () => {
        this.initMap();
      }
      document.head.appendChild(script);

      window.initMap = this.initMap.bind(this);
    }
  },
  methods: {
    handleCancel() {
      this.cancel(this.orderid)
    },

    async initMap() {
      // Google Maps API가 로드되면 호출되는 초기화 함수
      const position = this.positions[0];

      // eslint-disable-next-line
      const { Map } = await google.maps.importLibrary("maps");

      // 구글 맵 API에서 필요한 요소 불러와서 지도 객체 생성
      this.map = new Map(document.getElementById("map"), {
        zoom: 18,
        center: position,
        mapId: process.env.VUE_APP_GOOGLE_MAPS_MAP_ID
      });

      // 마커 추가
      // eslint-disable-next-line
      this.marker = new google.maps.Marker({
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

      console.log('Marker initialized', this.marker);
      // 마커 이동 함수 실행
      this.startMoving();
    },
    moveMarker() {
      // 현재 위치가 마지막 위치까지 도달하지 않았으면 이동
      if (this.currentIndex < this.positions.length - 1 && this.marker) {
         // 현재 마커의 위치 가져오기
        const currentLatLng = this.marker.getPosition();

        // LatLng 객체에서 숫자 좌표로 변환
        const currentPosition = {
          lat: currentLatLng.lat(),
          lng: currentLatLng.lng(),
        };

        const nextPosition = this.positions[this.currentIndex + 1];
        console.log("현재 위치:", currentPosition);
        console.log("다음 목표 위치:", nextPosition);


        // 각 좌표 간 차이를 계산
        const latDiff = nextPosition.lat - currentPosition.lat;
        const lngDiff = nextPosition.lng - currentPosition.lng;

        // 목표 지점에 도달할 때까지 일정 거리만큼 이동하도록 설정 step을 거리로 변경
        const distance = Math.sqrt(latDiff * latDiff + lngDiff * lngDiff);
        const step = Math.min(distance, 0.00003);  // 한 번에 이동할 거리로 계산

        // 이동할 비율로 새로운 위치 계산
        const latStep = (latDiff / distance) * step;
        const lngStep = (lngDiff / distance) * step;

        const newLat = currentPosition.lat + latStep;
        const newLng = currentPosition.lng + lngStep;

        // 새로운 위치로 마커 위치 업데이트
        const newPosition = { lat: newLat, lng: newLng };
        this.marker.setPosition(newPosition);

        // 지도 중심 업데이트
        this.map.setCenter(newPosition);

        // 목표 위치 도달 확인
        const latReached = Math.abs(newLat - nextPosition.lat) < 0.0001;
        const lngReached = Math.abs(newLng - nextPosition.lng) < 0.0001;

        // 목표 위치에 도달한 경우
        if (latReached && lngReached) {
          console.log(`목표 위치 도달: ${nextPosition.lat}, ${nextPosition.lng}`);
          this.currentIndex++; // 다음 위치로 이동
        }

        // 계속 이동
        if (this.currentIndex < this.positions.length - 1) {
          setTimeout(() => {
            this.moveMarker();
          }, 200);
        } else {
          console.log("모든 경로 이동 완료");
        }
      }
    },
    startMoving() {
      if (this.marker) {
        this.currentIndex = 0;  // 초기화
        this.moveMarker();  // 마커 이동 시작
      }
    },
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