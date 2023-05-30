// group create button [+] 그리기

// 컨테이너 요소와 SVG 요소, 선 요소를 선택합니다.
const container = document.getElementById("group-create-button");
const hLine = document.getElementById("horizontal-line");
const vLine = document.getElementById("vertical-line");

function updateCoordinates() {
  // 컨테이너의 크기를 가져옵니다.
  const containerRect = container.getBoundingClientRect();
  const containerWidth = containerRect.width;
  const containerHeight = containerRect.height;

  const hStartX = containerRect.left * 0.8 + containerRect.right * 0.2; // 시작점 x 좌표 (중심으로부터 왼쪽으로 40%)
  const hStartY = containerRect.top * 0.5 + containerRect.bottom * 0.5; // 시작점 y 좌표 (중심과 동일)
  const hEndX = containerRect.left * 0.2 + containerRect.right * 0.8; // 끝점 x 좌표 (중심으로부터 오른쪽으로 40%)
  const hEndY = containerRect.top * 0.5 + containerRect.bottom * 0.5; // 끝점 y 좌표 (중심과 동일)

  // 선의 좌표를 설정합니다.
  hLine.setAttribute("x1", hStartX);
  hLine.setAttribute("y1", hStartY);
  hLine.setAttribute("x2", hEndX);
  hLine.setAttribute("y2", hEndY);

  const vStartX = containerRect.left * 0.5 + containerRect.right * 0.5; // 시작점 x 좌표 (중심으로부터 왼쪽으로 40%)
  const vStartY = containerRect.top * 0.2 + containerRect.bottom * 0.8; // 시작점 y 좌표 (중심과 동일)
  const vEndX = containerRect.left * 0.5 + containerRect.right * 0.5; // 끝점 x 좌표 (중심으로부터 오른쪽으로 40%)
  const vEndY = containerRect.top * 0.8 + containerRect.bottom * 0.2; // 끝점 y 좌표 (중심과 동일)

  // 선의 좌표를 설정합니다.
  vLine.setAttribute("x1", vStartX);
  vLine.setAttribute("y1", vStartY);
  vLine.setAttribute("x2", vEndX);
  vLine.setAttribute("y2", vEndY);
}

// 초기화 시 좌표 업데이트
updateCoordinates();

// 리사이즈 이벤트 핸들러
window.addEventListener("resize", updateCoordinates);
