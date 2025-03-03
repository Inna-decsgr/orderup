<template>
  <div class="popup-content">
    <div class="flex items-center mb-3">
      <button @click="handleCancel" class="w-[40px] h-[40px] bg-white shadow-xl   rounded-full mr-3">
        <i class="fa-solid fa-xmark text-xl"></i>
      </button>
      <span class="font-bold">{{ isDelivering ? '주문하신 곳으로 가고 있어요' : '배달 완료' }}</span>
    </div>
    <div>
      <div id="map" style="width:100%; height:500px"></div>
    </div>
    <button v-if="!isDelivering" @click="confirm">배달 확인</button>
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
      isWaiting: false,
      isTracking: false,
      isDelivering: true
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
      this.isTracking = false;
      this.cancel(this.orderid)
    },

    async initMap() {
      // Google Maps API가 로드되면 호출되는 초기화 함수
      const position = this.positions[0];
      const position1 = this.positions[1]; 
      const position2 = this.positions[2]; 

      // eslint-disable-next-line
      const { Map } = await google.maps.importLibrary("maps");

      // 구글 맵 API에서 필요한 요소 불러와서 지도 객체 생성
      this.map = new Map(document.getElementById("map"), {
        zoom: 18,
        center: position,
        mapId: process.env.VUE_APP_GOOGLE_MAPS_MAP_ID
      });

      // 배달지 표시
      // eslint-disable-next-line
      this.marker1 = new google.maps.Marker({
        map: this.map,
        position: position1,
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
      // eslint-disable-next-line
      this.marker2 = new google.maps.Marker({
        map: this.map,
        position: position2,
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

      // 마커 추가
      // eslint-disable-next-line
      this.marker = new google.maps.Marker({
        map: this.map,
        position: position,
        icon: {
          url: "/motocycle.svg",
          // eslint-disable-next-line
          scaledSize: new google.maps.Size(60, 60), 
          // eslint-disable-next-line
          anchor: new google.maps.Point(20, 40), 
        }
      });

      this.startMoving();
    },
    moveMarker() {// 현재 위치가 마지막 위치까지 도달하지 않았으면 이동
      if (this.currentIndex < this.positions.length - 1 && this.marker && !this.isWaiting && this.isTracking) {
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
          this.currentIndex++;


          // 첫 번째 배달지에서 5초 대기
          if (this.currentIndex === 1) {
            console.log("첫 번째 배달지 도착, 5초 대기중....");
            this.isWaiting = true;
            setTimeout(() => {
              this.isWaiting = false;
              if (this.isTracking) this.moveMarker();
            }, 5000);
            return;
          }

          if (this.currentIndex === this.positions.length - 1) {
            console.log("배달을 마쳤습니다.");
            this.isDelivering = false;
            return;
          }

          if (this.isTracking) this.moveMarker();  // 다음 위치로 이동
        } else {
          setTimeout(() => {
            if (this.isTracking) this.moveMarker();
          }, 200);
        }
      }
    },
    startMoving() {
      if (this.marker) {
        this.currentIndex = 0;  // 초기화
        this.isTracking = true;
        this.moveMarker();  // 마커 이동 시작
      }
    },
    confirm() {
      this.$emit('confirm');
      this.cancel(this.orderid)
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