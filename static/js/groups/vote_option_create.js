const optionContainer = document.getElementById("options-container")
const plusBtn = document.getElementById("plus-button")
const optionInput = document.getElementById("options")

// plus버튼 클릭 시 input tag 추가
plusBtn.addEventListener('click', function() {
  // input tag와 삭제버튼 div에 담아서 선택지에 추가
  const optionDiv = document.createElement('div')
  // 위에 있는 input tag 복제
  const copyInput = optionInput.cloneNode(true)
  copyInput.value = ''
  const deleteBtn = document.createElement('button')
  deleteBtn.type = 'button'
  deleteBtn.textContent = '삭제'
  optionDiv.appendChild(copyInput)
  optionDiv.appendChild(deleteBtn)
  optionContainer.appendChild(optionDiv)

  // 삭제 버튼 클릭 시 div 삭제
  deleteBtn.addEventListener('click', function() {
    optionDiv.remove()
  })
})