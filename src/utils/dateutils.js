// src/utils/dateUtils.js

export function formatDate(dateString) {
  const date = new Date(dateString);

  const options = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true, // 12시간 형식 (오전/오후 처리)
  };

  const formattedDate = new Intl.DateTimeFormat('ko-KR', options).format(date);
  
  // 여기서 오전/오후를 처리하는 부분을 제거
  // 시간에 대해 두 번 오전/오후가 출력되는 문제를 방지

  return formattedDate;
}
