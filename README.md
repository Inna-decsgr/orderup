# Orderup

### 프로젝트 이름
Orderup

### 프로젝트 설명
OrderUp은 사용자가 다양한 가게에서 음식을 주문하고 배달받을 수 있는 웹 애플리케이션이다.
이 프로젝트는 Vue.js 기반의 프론트엔드와 Flask 기반의 백엔드로 구축되었으며, Vuex를 활용해 상태를 효율적으로 관리하고 배달 상태를 업데이트할 수 있도록 설계되었다.
백엔드는 Flask와 MySQL을 사용해 데이터 관리와 성능을 최적화하였으며, RESTful API를 통해 프론트엔드와 원활하게 연동된다.
또한, 사용자 경험(UX), 데이터 흐름, 보안을 고려하였으며, 효율적인 API 연동과 데이터 제공에 중점을 두었다.


### 사용 기술
* 프론트엔드
  * **Vue.js**: 사용자 인터페이스 구축
  * **Vuex**: 상태 관리
  * **Vue Router**: 라우팅 관리
  * **Axios**: HTTP 클라이언트
  * **TailwindCSS & Bootstrap**: UI 스타일링
  * **Swiper & Chart.js**: 슬라이더 및 데이터 시각화
* 백엔드
  * **Flask, Django**: 프레임워크
  * **MySQL**: 데이터베이스
  * **Python**: 언어
  * **Django Authentication, Django ORM, Django URLs & Views, Django Static & Media**: 라이브러리
  * **MySQL**: 데이터베이스


### 구현 사항
* **사용자 기능(고객)**
  * **회원가입, 로그인, 사용자 정보 수정**
    * 신규 회원가입 및 기존 사용자 로그인
    * 로그인 후 사용자 정보 수정 가능
  * **가게 검색 및 가게 찜하기**
    * 키워드로 메뉴 또는 가게 검색
    * 최근 검색어 삭제 기능 제공
    * 가게 찜하기 및 찜한 가게 목록에서 확인 가능
  * **할인 쿠폰 발급 및 사용**
    * 할인 쿠폰 발급 후 결제 시 적용 가능
  * **장바구니 관리**
    * 같은 가게의 메뉴만 장바구니에 추가 가능
    * 장바구니에서 개별 메뉴 삭제 가능
  * **주문 및 결제**
    * 결제 후 주문 내역에 자동 추가
    * 상세 주문 정보 조회 가능
  * **리뷰 작성 및 수정**
    * 배달 완료된 주문에 한해 리뷰 작성 가능
    * 작성한 리뷰 수정 가능
* 사업자 기능(사장님)
  * **회원가입 및 가게 등록**
    * 회원가입 시 사업자등록번호 입력 시 사장님 계정으로 가입 가능
    * 사장님 계정은 가게 입점 신청 가능
  * **가게 정보 관리**
    * 입점 신청한 가게의 정보 수정 가능
    * 등록된 모든 가게 현황 관리 가능
  * **메뉴 관리**
    * 메뉴 추가, 수정 및 삭제 가능
  * **주문 관리**
    * 주문 접수 및 처리(접수, 거절, 조리 완료, 라이더 배정, 배달 완료)
* 배달 기능
  * **배달원 정보 확인 후 라이더 배정**
  * **배달 상태 업데이트**
    * "픽업 완료" > "배달중" > "배달 완료"
 
