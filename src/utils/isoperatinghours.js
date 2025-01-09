export function isOperatingHour(storeoperating) {
  if (!storeoperating) return {isOperting: false, nextStart: null};

  const now = new Date();
  const currentHour = now.getHours();
  const currentMinute = now.getMinutes();


  // 전달받은 운영 시간 분리
  const [start, end] = storeoperating.split(" - ");

  // 문자열을 시간으로 변환하기 11:00 -> { hour: 11, minute: 0 }
  const [startHour, startMinute] = start.split(":").map(Number);
  const [endHour, endMinute] = end.split(":").map(Number);

  // 현재 시간이 운영시간 이후인지 확인하기
  const isAfterOperating = currentHour > startHour || (currentHour === startHour && currentMinute >= startMinute);

  // 현재 시간이 종료 시간 이전인지 확인하기
  const isBeforeOperating = currentHour < endHour || (currentHour === endHour && currentMinute <= endMinute)

  const isOperating = isAfterOperating && isBeforeOperating;

  return {
    isOperating,
    nextStart: !isOperating ? null : `${String(startHour).padStart(2, '0')}:${String(startMinute).padStart(2, '0')}`
  }
}