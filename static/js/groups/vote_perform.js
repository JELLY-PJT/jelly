const switchBtns = document.querySelectorAll('.switch-btn')

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
  const voteId = form.dataset.voteId
  const voteOverlap = form.dataset.voteOverlap // 중복투표 여부
  const options = form.querySelectorAll('.option')
  const selectedList = []
  const optionsInput = document.getElementById(`${voteId}-options`)
  options.forEach(option => {
    const optionId = option.dataset.optionId
    const userExist = option.dataset.userExist
    if (userExist === "true") {
      // ✅여기서 선택 표시 넣어야함
      selectedList.push(optionId)
      optionsInput.value = JSON.stringify(selectedList)
    }
    option.addEventListener('click', function() {
      // 선택했던 option을 클릭 시 제거
      if (selectedList.includes(optionId)) {
        // ✅여기서 선택 표시 없애야함
        const index = selectedList.findIndex(id => id === optionId)
        selectedList.splice(index, 1)
        optionsInput.value = JSON.stringify(selectedList)
      } else {
        // false인 경우 selectedList 비우기
        if (voteOverlap === false) {
          // ✅여기서 selectedList에 있는 인자 모두 선택 표시 없애야함
          selectedList = []
        }
        if (!selectedList.includes(optionId)) {
          // ✅여기서 선택 표시 넣어야함
          selectedList.push(optionId)
        }
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