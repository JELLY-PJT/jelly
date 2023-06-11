const switchBtns = document.querySelectorAll('.switch-btn')

// 투표 다시하기 버튼 클릭 시 투표 수행 Div 보이도록 함
switchBtns.forEach(btn => {
  const voteId = btn.dataset.voteId
  const readVoteDiv = document.getElementById(`for-read-vote-${voteId}`)
  const performVoteDiv = document.getElementById(`for-perform-vote-${voteId}`)
  btn.addEventListener('click', function() {
    readVoteDiv.style.display = 'none'
    performVoteDiv.style.display = 'block'
  })
})

const votePerformForms = document.querySelectorAll('.vote-perform-form')

votePerformForms.forEach(form => {
  const voteId = form.dataset.voteId // 투표 pk
  const voteOverlap = form.dataset.voteOverlap // 중복투표 여부
  const options = form.querySelectorAll('.option') // 현재 form의 선택지들
  let selectedList = []
  const optionsInput = document.getElementById(`${voteId}-options`) // selectedList를 담을 input tag
  options.forEach(option => {
    const optionId = option.dataset.optionId
    const userExist = option.dataset.userExist
    const svgElement = option.querySelector('svg') // SVG 이미지 요소 선택
    if (userExist === "true") {
      // ✅여기서 선택 표시 넣어야함
      option.classList.add('selected') // 선택된 옵션에 selected 클래스 추가
      svgElement.classList.remove('hidden') // SVG 이미지 표시
      option.classList.remove('blank-vote');
      selectedList.push(optionId)
      optionsInput.value = JSON.stringify(selectedList)

    }
    option.addEventListener('click', function() {
      // 선택했던 option을 클릭 시 제거
      if (selectedList.includes(optionId)) {
        // ✅여기서 선택 표시 없애야함
        option.classList.remove('selected') // 선택 취소 시 selected 클래스 제거
        svgElement.classList.add('hidden') // SVG 이미지 숨김
        option.classList.add('blank-vote');
        const index = selectedList.findIndex(id => id === optionId)
        selectedList.splice(index, 1)
        optionsInput.value = JSON.stringify(selectedList)
      } else {
        // false인 경우 selectedList 비우기
        if (voteOverlap == "false") {
          // ✅여기서 selectedList에 있는 인자 모두 선택 표시 없애야함
          options.forEach(opt => {
            opt.classList.remove('selected') // 모든 옵션에서 선택 표시 제거
            opt.querySelector('svg').classList.add('hidden') // 모든 SVG 이미지 숨김
            opt.classList.add('blank-vote');
          })
          selectedList = []
        }
        // ✅여기서 선택 표시 넣어야함
        option.classList.add('selected') // 선택된 옵션에 selected 클래스 추가
        svgElement.classList.remove('hidden') // SVG 이미지 표시
        option.classList.remove('blank-vote');

        selectedList.push(optionId)
        optionsInput.value = JSON.stringify(selectedList)
      }
    })
  })
})

// vote 조회수 
const voteHitsForm = document.querySelectorAll('.vote-hits')
// console.log(voteHitsForm)
voteHitsForm.forEach(form => {
  form.addEventListener('click', function(event) {
    event.preventDefault()
    const voteId = form.dataset.voteId
    const csrftoken = form.querySelector('[name=csrfmiddlewaretoken]').value
    axios({
      method: 'POST',
      url: `/groups/votes/${voteId}/hits/`,
      headers: {'X-CSRFToken': csrftoken,}
    })
      .then((response) => {
        const voteHitsCount = document.getElementById(`${voteId}-hits-count`)
        voteHitsCount.textContent = response.data.vote_hits
      })
  })
})


// progressbar
const options = document.querySelectorAll('[id^="calculationResult-"]');
options.forEach(function(option) {
  let selectUsersCount = parseInt(option.getAttribute("data-select-users-count"));
  let voteSelectCount = parseInt(option.getAttribute("data-voteselect-count"));
  let result = (selectUsersCount / voteSelectCount) * 100;
  result = result.toFixed(1); // 소수점 한 자리까지 제한
  option.innerText = result + "%";
  option.style.width = result + "%";
});
