
// group create button [+] 그리기

// // 컨테이너 요소와 SVG 요소, 선 요소를 선택합니다.
// const container = document.getElementById("group-create-button");
// const hLine = document.getElementById("horizontal-line");
// const vLine = document.getElementById("vertical-line");

// function updateCoordinates() {
//   // 컨테이너의 크기를 가져옵니다.
//   const containerRect = container.getBoundingClientRect();
//   const containerWidth = containerRect.width;
//   const containerHeight = containerRect.height;

//   const hStartX = containerRect.left * 0.8 + containerRect.right * 0.2; // 시작점 x 좌표 (중심으로부터 왼쪽으로 40%)
//   const hStartY = containerRect.top * 0.5 + containerRect.bottom * 0.5; // 시작점 y 좌표 (중심과 동일)
//   const hEndX = containerRect.left * 0.2 + containerRect.right * 0.8; // 끝점 x 좌표 (중심으로부터 오른쪽으로 40%)
//   const hEndY = containerRect.top * 0.5 + containerRect.bottom * 0.5; // 끝점 y 좌표 (중심과 동일)

//   // 선의 좌표를 설정합니다.
//   hLine.setAttribute("x1", hStartX);
//   hLine.setAttribute("y1", hStartY);
//   hLine.setAttribute("x2", hEndX);
//   hLine.setAttribute("y2", hEndY);

//   const vStartX = containerRect.left * 0.5 + containerRect.right * 0.5; // 시작점 x 좌표 (중심으로부터 왼쪽으로 40%)
//   const vStartY = containerRect.top * 0.2 + containerRect.bottom * 0.8; // 시작점 y 좌표 (중심과 동일)
//   const vEndX = containerRect.left * 0.5 + containerRect.right * 0.5; // 끝점 x 좌표 (중심으로부터 오른쪽으로 40%)
//   const vEndY = containerRect.top * 0.8 + containerRect.bottom * 0.2; // 끝점 y 좌표 (중심과 동일)

//   // 선의 좌표를 설정합니다.
//   vLine.setAttribute("x1", vStartX);
//   vLine.setAttribute("y1", vStartY);
//   vLine.setAttribute("x2", vEndX);
//   vLine.setAttribute("y2", vEndY);
// }

// // 초기화 시 좌표 업데이트
// updateCoordinates();

// // 리사이즈 이벤트 핸들러
// window.addEventListener("resize", updateCoordinates);





class CreateGroup {
  $target = null;
  $modalButton = null;

  constructor($target) {
    this.$target = $target;

    // 모달 열기 버튼 생성
    this.$modalButton = document.createElement("button");
    this.$modalButton.addEventListener("click", this.onOpenModal.bind(this), false);

    // 모달 인스턴스 생성
    this.info = new Modal({
      $target: this.$target,
      visible: false,
    });

    // #CreateGroup의 <div>를 클릭하면 모달 열기
    this.$target.addEventListener("click", this.onOpenModal.bind(this), false);
  }

  // 모달 열기 이벤트 핸들러
  onOpenModal() {
    this.info.setState();
  }
}

window.onload = () => {
  // 앱 인스턴스 생성
  new CreateGroup(document.querySelector("#group-create-button"));
};


// 모달 클래스
class Modal {
  $info = null;

  constructor({ $target, visible }) {

    // 모달 레이어 생성
    this.$modalLayer = document.createElement("div");
    this.$modalLayer.className = "modal-layer";
    document.querySelector("main").appendChild(this.$modalLayer);

    // 모달 정보를 담을 div 요소 생성
    const $info = document.createElement("div");
    $info.id = "CreateGroupModal";
    this.$info = $info;
    this.$modalLayer.appendChild($info);

    // 모달 레이어 클릭 이벤트 핸들러 등록
    this.$modalLayer.addEventListener("click", this.onModalLayerClick.bind(this), false);


    // 모달 상태 초기화
    this.visible = visible;

    this.render();
  }

  // 모달 상태 변경 메서드
  setState() {
    this.visible = !this.visible;

    if (this.visible) {
      // 모달 표시될 때 모달 레이어 클릭 이벤트 핸들러 등록
      this.$modalLayer.addEventListener("click", this.onModalLayerClick.bind(this), false);
    } else {
      // 모달 숨겨질 때 모달 레이어 클릭 이벤트 핸들러 제거
      this.$modalLayer.removeEventListener("click", this.onModalLayerClick.bind(this), false);
    }

    this.render();
  }

  // 모달 닫기 메서드
  closeInfo() {
    console.log('모달 닫기 메서드 호출됨');
    this.visible = false;
    this.render();
  }

  // 모달 레이어 클릭 이벤트 핸들러
  onModalLayerClick(event) {
    // 클릭한 요소가 모달 레이어 자체인 경우에만 모달을 닫도록 처리
    if (event.target === this.$modalLayer) {
      this.closeInfo();
    }
  }

  // 모달 렌더링 메서드
  render() {
    // const src =
    //   "https://raw.githubusercontent.com/mooyeon-choi/kinetic-typography-7/master/images/kinetic-typography-7-example.gif";
    
    if (this.visible) {
      console.log('표시하는 중');
      this.$info.innerHTML = `
        <article class="content-wrapper">
          <button class="close" style="width:30px;height30px;background-color:black;color:white;">x</button>
          <p>  나는 모달입니다.
            그룹을 만들어보자 
            여기에 그룹 생성 폼을 올려주세요
            css 요소는 __groups.css 의 #CreateGroupModal 에서 조절해 주세요 ^^</li>
          </p>
        </article>`;

        // create_group.html 완성 시 위의 if 블록을 삭제하고 아래의 if 블록을 활성화 

    // if (this.visible) {
    //   this.$info.innerHTML = `          <header class="title">
     //       <button class="close" style="width:30px;height30px;background-color:black;color:white;">x</button>
       //     </header>{% include 'groups/create_group.html' %}`;

      const closeModal = this.$info.querySelector(".close");
      closeModal.addEventListener("click", this.closeInfo.bind(this), false);
      this.$info.style.display = "block";
      this.$modalLayer.style.display = "block";

    } else {
      console.log('모달 지우는 중 ');
      console.log(this.$info);
      this.$info.style.display = "none";
      this.$modalLayer.style.display = "none";
      console.log(this.$info);
    
    }
  }
}
