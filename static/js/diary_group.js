// 공유된 다이어리 댓글 좋아요 비동기 처리 js

const commentLikeForms = document.querySelectorAll('.comment-like-forms')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

commentLikeForms.forEach((form) => {
  form.addEventListener('submit', function(event) {
    event.preventDefault()
    const commentId = event.target.dataset.commentId
    const groupId = event.target.dataset.groupId
    const diaryId = event.target.dataset.diaryId

    axios({
      method: 'post',
      url: `/diaries/${groupId}/${diaryId}/comments/${commentId}/like/`,
      headers: {
        'X-CSRFToken': csrftoken,
      }
    })
      .then((response) => {
        const commentLikeBtn = document.querySelector(`#comment-like-btn-${commentId}`)
        
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
})