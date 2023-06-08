const inviteBtn = document.getElementById('invite-btn')
groupId = inviteBtn.dataset.groupId

function copyLink() {
  const url = `http://127.0.0.1:8000/groups/${groupId}/join/`
  navigator.clipboard.writeText(url)
  .then(function() {
    alert("초대링크가 복사되었습니다.")
  })
  .catch(function(error) {
    /* 복사 실패 시 에러 메시지를 표시합니다. */
    alert("주소 복사에 실패했습니다.");
    console.error(error);
  });
}