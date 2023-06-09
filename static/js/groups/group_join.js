const modal = document.getElementById('passwordModal')
const modalBtn = document.getElementById('modal-btn')

window.addEventListener('load', function() {
  modalBtn.click()
})

const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
const groupId = modal.dataset.groupId

document.querySelector('.join-form').addEventListener('submit', function(event) {
  const password = document.getElementById('password').value
  
  event.preventDefault()
  console.log(password)
  axios({
    method: 'post',
    url: ``,
    headers: {
      'X-CSRFToken': csrftoken,
    },
    data: {'password': password,}
  })
    .then(response => {
      if (response.data.message) {
        alert(response.data.message)
      } else {
        location.reload()
      }
    })
})
  