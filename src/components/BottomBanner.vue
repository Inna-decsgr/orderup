<template>
  <div class="banner">
    <div>
      <p>사업자정보확인 | 이용약관 | 전자금융거래이용약관 | 개인정보처리방침 | 리뷰운영정책 | 데이터제공정책 | 소비자분쟁해결기준</p>
      <p><strong>(주)오더업</strong></p>
      <p>대표이사 홍길동 | 사업자등록번호 123-45-67890<br/>
      통신판매업 서울 동동 -0212 | 호스팅서비스제공자 (주)오더업<br/>
      Help@orderup.com | 서울특별시 동동구 아리대로 2 길동빌딩<br/>
      전자금융분쟁처리 Tel 1500-2836(유료), 020-473-2903(무료)<br/>
      Fax 050-2020-0500</p>
    </div>
    <div class="customer_center">
      <div class="customer_box">
        <p>고객센터(대표)<br/>
        1500-2836<br/>
        24시간 운영, 연중무휴</p>
      </div>
      <div class="customer_box">
        <p>고객센터(배달)<br/>
        1500-0035<br/>
        오전 9:00 ~ 다음 날 오전 1:00</p>
      </div>
    </div>
    <div>
      <p>(주)오더업은 통신판매중개자로 거래 당사자가 아니므로, 판매자가 등록한 상품정보 및 거래 등에 대해 책임을 지지 않습니다. 단, (주)오더업이 판매자로 등록 판매한 상품은 판매자로서 책임을 부담합니다.</p>
    </div>
  </div>
</template>

<style>
.banner {
  background-color: rgb(236, 236, 236);
  padding: 20px;
  color: rgb(129, 129, 129);
  font-weight: bold;
}

.customer_center {
  display: flex;
  justify-content: center; 
}
.customer_box {
  width: 48%;
  border: 1px solid #ccc;
  margin-bottom: 20px;
  padding: 10px;
}

.customer_box:last-child {
  border-left: none; 
}
</style>