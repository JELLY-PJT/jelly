const createBtn = document.getElementById('dropdownDefaultButton')
const dialBtn = document.getElementById('dial-btn')

if (window.scrollY >= 240) {
  dialBtn.classList.remove('hidden')
}

window.addEventListener('scroll', function() {
    if (this.scrollY >= 240) {
    createBtn.style.display = 'none'
    dialBtn.classList.remove('hidden')
  } else {
    createBtn.style.display = 'flex'
    dialBtn.classList.add('hidden')
  }
})
