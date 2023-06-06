const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value


// 감정표현 비동기 처리 js
const emotionForm = document.querySelectorAll('.emotion-form')

emotionForm.forEach(form => {
  form.addEventListener('submit', function(event) {
    event.preventDefault()
    const groupId = event.target.dataset.groupId
    const diaryId = event.target.dataset.diaryId
    const emotionValue = event.target.dataset.emotion

    axios({
      method: 'post',
      url: `/diaries/${groupId}/${diaryId}/emotes/${emotionValue}/`,
      headers: {
        'X-CSRFToken': csrftoken,
      }
    })
      .then(response => {
        let total = 0
        emotionForm.forEach(newForm => {
          if (response.data.delete) {
            if (form == newForm) {
              form.parentElement.classList.remove('selected-emotion')
              newForm.querySelector('.emotion-count').textContent = Number(newForm.querySelector('.emotion-count').textContent) - 1
            } 
          } else {
            if (form != newForm && newForm.parentElement.classList.contains('selected-emotion') ) {
              newForm.parentElement.classList.remove('selected-emotion')
              newForm.querySelector('.emotion-count').textContent = Number(newForm.querySelector('.emotion-count').textContent) - 1
            } else if (form == newForm) {
              form.parentElement.classList.add('selected-emotion')
              newForm.querySelector('.emotion-count').textContent = Number(newForm.querySelector('.emotion-count').textContent) + 1
            }
          }

          total += Number(newForm.querySelector('.emotion-count').textContent)
        })

        document.querySelector('.emotion-total-count').textContent = total
      })
  })
})


const commentArea = document.querySelectorAll('.comment-area')

commentArea.forEach(area => {
  const commentId = area.dataset.commentId
  const groupId = area.dataset.groupId
  const diaryId = area.dataset.diaryId

  // 공유된 다이어리 댓글 좋아요 비동기 처리 js
  const commentLikeForm = area.querySelector('.comment-like-form')

  commentLikeForm.addEventListener('submit', function(event) {
    event.preventDefault()
    axios({
      method: 'post',
      url: `/diaries/${groupId}/${diaryId}/comments/${commentId}/like/`,
      headers: {
        'X-CSRFToken': csrftoken,
      }
    })
      .then((response) => {
        const commentLikeBtn = area.querySelector('.comment-like-btn')
        
        commentLikeBtn.children[1].textContent = response.data.comment_like_users

        if (response.data.is_liked) {
          commentLikeBtn.children[0].style.fill = '#E02424'
        } else {
          commentLikeBtn.children[0].style.fill = 'none'
        }
      })
      .catch((error) => {
        console.log(error.response)
      })
  })

  // 댓글 수정 비동기 처리
  const commentUpdateBtn = area.querySelectorAll('.comment-update-btn')
  
  if (commentUpdateBtn) {
    commentUpdateBtn.forEach(btn => {
      btn.addEventListener('click', function(event) {
        const updateForm = area.querySelector('#comment-update-form')
        const commentContentTag = area.querySelector('.comment-comment')
        let commentContent = commentContentTag.textContent

        if (updateForm.classList.contains('hidden')) {
          updateForm.classList.remove('hidden')
          commentContentTag.classList.add('hidden')
          btn.textContent = '취소'
        } else {
          updateForm.classList.add('hidden')
          commentContentTag.classList.remove('hidden')
          btn.textContent = '댓글 수정'
        }
        
  
        updateForm.children[1].value = commentContent

        updateForm.addEventListener('submit', function(event) {
          event.preventDefault()
          const formData = new FormData(updateForm)

          axios({
            method: 'POST',
            url: `/diaries/${groupId}/${diaryId}/comments/${commentId}/update/`,
            headers: {'X-CSRFToken': csrftoken},
            data: formData,
          })
            .then(response => {
              let commentContent = area.querySelector('.comment-comment')

              commentContent.textContent = response.data.content
              updateForm.classList.add('hidden')
              commentContentTag.classList.remove('hidden')
              btn.textContent = '댓글 수정'
            })
        })
      })
    })
  }

})