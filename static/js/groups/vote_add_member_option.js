const addBtn = document.getElementById('add-member-option')
if (addBtn) {
  const addOptionContainer = document.getElementById('add-option-div')
  
  addBtn.addEventListener('click', function() {
    const optionDiv = document.createElement('div')
    const optionInput = document.createElement('input')
    optionInput.name = 'options'
    // tailwind modal 가져오면 있는 class 적용
    optionInput.classList.add('bg-gray-50', 'border', 'border-gray-300', 'text-gray-900', 'text-sm', 'rounded-lg', 'focus:ring-blue-500', 'focus:border-blue-500', 'block', 'p-2.5', 'dark:bg-gray-600', 'dark:border-gray-500', 'dark:placeholder-gray-400', 'dark:text-white')
    const deleteBtn = document.createElement('button')
    deleteBtn.type = 'button'
    deleteBtn.textContent = '삭제'
    optionDiv.appendChild(optionInput)
    optionDiv.appendChild(deleteBtn)
    addOptionContainer.appendChild(optionDiv)
  
    // 삭제 버튼 클릭 시 div 삭제
    deleteBtn.addEventListener('click', function() {
      optionDiv.remove()
    })
  })
}
