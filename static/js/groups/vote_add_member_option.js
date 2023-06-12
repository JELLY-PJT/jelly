document.addEventListener('DOMContentLoaded', function() {
  const addBtns = document.querySelectorAll('.add-member-option')
  console.log(addBtns)
  addBtns.forEach(addBtn => {
    const voteId = addBtn.dataset.voteId
    const addOptionForm = document.getElementById(`add-option-form-${voteId}`)
    const addOptionContainer = document.getElementById(`add-option-div-${voteId}`)
    
    addBtn.addEventListener('click', function() {
      // 항목추가 버튼 클릭 시 form 보이게 함
      addOptionForm.style.display = 'block'
      const optionDiv = document.createElement('div')
      const optionInput = document.createElement('input')
      optionInput.name = 'options'
      // tailwind modal 가져오면 있는 class 적용
      // optionInput.classList.add('bg-gray-50', 'border', 'border-gray-300', 'text-gray-900', 'text-sm', 'rounded-lg', 'focus:ring-blue-500', 'focus:border-blue-500', 'block', 'p-2.5', 'dark:bg-gray-600', 'dark:border-gray-500', 'dark:placeholder-gray-400', 'dark:text-white')
      optionInput.type = 'text'
      optionInput.classList.add('optionplus-input', 'bg-gray-50', 'border-gray-300')
      const deleteBtn = document.createElement('button')
      deleteBtn.type = 'button'
      deleteBtn.classList.add('margin-left--10px')
      deleteBtn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#ff5656" class="w-6 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" /></svg>'
      optionDiv.appendChild(optionInput)
      optionDiv.appendChild(deleteBtn)
      addOptionContainer.appendChild(optionDiv)
    
      // 삭제 버튼 클릭 시 div 삭제
      deleteBtn.addEventListener('click', function() {
        optionDiv.remove()
      })
    })
  })
})