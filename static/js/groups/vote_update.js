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
        const titleInput = updateForm.querySelector('#id_title')
        titleInput.value = response.data.title
        const deadlineInput = updateForm.querySelector('#id_deadline')
        let deadline = new Date(response.data.deadline)
        new Date(deadline.setHours(deadline.getHours() + 9)).toISOString().slice(0, -5)
        deadlineInput.value = new Date(deadline).toISOString().slice(0, -5)
        const overlapInput = updateForm.querySelector('#id_is_overlap')
        overlapInput.checked = response.data.is_overlap
        const annonyInput = updateForm.querySelector('#id_is_annony')
        annonyInput.checked = response.data.is_annony
        const addibleInput = updateForm.querySelector('#id_is_addible')
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
    optionDiv.classList.add('flex-row')
    const optionInput = document.createElement('input')
    optionInput.name = 'options'
    // optionInput.classList.add('bg-gray-50', 'border', 'border-gray-300', 'text-gray-900', 'text-sm', 'rounded-lg', 'focus:ring-blue-500', 'focus:border-blue-500', 'block', 'p-2.5', 'dark:bg-gray-600', 'dark:border-gray-500', 'dark:placeholder-gray-400', 'dark:text-white')
    optionInput.type = 'text'
    optionInput.classList.add('optionplus-input', 'bg-gray-50', 'border-gray-300')
    const deleteBtn = document.createElement('button')
    deleteBtn.classList.add('margin-left--10px')
    deleteBtn.type = 'button'
    // deleteBtn.textContent = '삭제'
    deleteBtn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#ff5656" class="w-6 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" /></svg>'
    optionDiv.appendChild(optionInput)
    optionDiv.appendChild(deleteBtn)
    updateOptionDiv.appendChild(optionDiv)
    
    // 삭제 버튼 클릭 시 div 삭제
    deleteBtn.addEventListener('click', function() {
      optionDiv.remove()
    })
  })
})

const originOptionInputs = document.querySelectorAll('.originOptionInput')
  
originOptionInputs.forEach(originOptionInput => {
  const originDeleteBtn = originOptionInput.querySelector('.originDeleteBtn')
  
  originDeleteBtn.addEventListener('click', function() {
    originOptionInput.remove()
  })
})