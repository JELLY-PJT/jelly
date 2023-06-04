const updateBtn = document.getElementById('vote-update')
const voteId = updateBtn.dataset.voteId
const updateOptionDiv = document.getElementById('update-option-container')

// 수정버튼 눌렀을 때 기존 정보 가져와 input value로 넣기
updateBtn.addEventListener('click', function() {
  axios({
    method: 'get',
    url: `/groups/votes/${voteId}/`
  })
    .then((response) => {
      const titleInput = document.getElementById('id_title')
      titleInput.value = response.data.title
      const deadlineInput = document.getElementById('id_deadline')
      deadlineInput.value = response.data.deadline
      const overlapInput = document.getElementById('id_is_overlap')
      overlapInput.value = response.data.is_overlap
      const annonyInput = document.getElementById('id_is_annony')
      annonyInput.value = response.data.is_annony
      const addibleInput = document.getElementById('id_is_addible')
      addibleInput.value = response.data.is_addible

      response.data.options.forEach(option => {
        const originOptionInput = document.createElement('input')
        originOptionInput.name = 'options'
        // tailwind modal 가져오면 있는 class 적용
        originOptionInput.classList.add('bg-gray-50', 'border', 'border-gray-300', 'text-gray-900', 'text-sm', 'rounded-lg', 'focus:ring-blue-500', 'focus:border-blue-500', 'block', 'p-2.5', 'dark:bg-gray-600', 'dark:border-gray-500', 'dark:placeholder-gray-400', 'dark:text-white')
        originOptionInput.value = option
        updateOptionDiv.appendChild(originOptionInput)
      });
    })
})

// 항목 추가 누르면 새로운 input tag생성
const newOptionBtn = document.getElementById('new-option-button')
newOptionBtn.addEventListener('click', function() {
  // input tag와 삭제버튼 div에 담아서 선택지에 추가
  const optionDiv = document.createElement('div')
  const optionInput = document.createElement('input')
  optionInput.name = 'options'
  optionInput.classList.add('bg-gray-50', 'border', 'border-gray-300', 'text-gray-900', 'text-sm', 'rounded-lg', 'focus:ring-blue-500', 'focus:border-blue-500', 'block', 'p-2.5', 'dark:bg-gray-600', 'dark:border-gray-500', 'dark:placeholder-gray-400', 'dark:text-white')
  
  const deleteBtn = document.createElement('button')
  deleteBtn.type = 'button'
  deleteBtn.textContent = '삭제'
  optionDiv.appendChild(optionInput)
  optionDiv.appendChild(deleteBtn)
  updateOptionDiv.appendChild(optionDiv)

  // 삭제 버튼 클릭 시 div 삭제
  deleteBtn.addEventListener('click', function() {
    optionDiv.remove()
  })
})