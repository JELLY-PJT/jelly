const optionContainer = document.getElementById("options-container")
const plusBtn = document.getElementById("plus-button")
const optionInput = document.getElementById("options")

// plus버튼 클릭 시 input tag 추가
plusBtn.addEventListener('click', function() {
  // input tag와 삭제버튼 div에 담아서 선택지에 추가
  const optionDiv = document.createElement('div')
  optionDiv.classList.add('flex-row')
  // 위에 있는 input tag 복제
  const copyInput = optionInput.cloneNode(true)
  copyInput.value = ''
  const deleteBtn = document.createElement('button')
  deleteBtn.classList.add('margin-left--10px')
  deleteBtn.type = 'button'
  // deleteBtn.textContent = '삭제'
  deleteBtn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#ff5656" class="w-6 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" /></svg>';
  optionDiv.appendChild(copyInput)
  optionDiv.appendChild(deleteBtn)
  optionContainer.appendChild(optionDiv)

  // 삭제 버튼 클릭 시 div 삭제
  deleteBtn.addEventListener('click', function() {
    optionDiv.remove()
  })
})