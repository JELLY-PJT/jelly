const updateBtn = document.querySelectorAll('.vote-update')

// 수정버튼 눌렀을 때 기존 정보 가져와 input value로 넣기
updateBtn.forEach(btn => {
  btn.addEventListener('click', function() {
    const voteId = btn.dataset.voteId
    const updateForm = document.getElementById(`vote-update-form-${voteId}`)
    axios({
      method: 'get',
      url: `/groups/votes/${voteId}/`
    })
      .then((response) => {
        const titleInput = updateForm.children[1].children[1]
        titleInput.value = response.data.title
        const deadlineInput = updateForm.children[2].children[1]
        let deadline = new Date(response.data.deadline)
        new Date(deadline.setHours(deadline.getHours() + 9)).toISOString().slice(0, -5)
        deadlineInput.value = new Date(deadline).toISOString().slice(0, -5)
        const overlapInput = updateForm.children[3].children[1]
        overlapInput.checked = response.data.is_overlap
        const annonyInput = updateForm.children[4].children[1]
        annonyInput.checked = response.data.is_annony
        const addibleInput = updateForm.children[5].children[1]
        addibleInput.checked = response.data.is_addible
      })
  })
})

// 항목 추가 누르면 새로운 input tag생성
const newOptionBtn = document.querySelectorAll('.new-option-button')
newOptionBtn.forEach(btn => {
  const voteId = btn.dataset.voteId
  const updateOptionDiv = document.getElementById(`update-option-container-${voteId}`)
  btn.addEventListener('click', function() {
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
})