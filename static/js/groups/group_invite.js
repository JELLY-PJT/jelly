function copyToClipboard(text) {
  const textField = document.createElement('textarea');
  textField.value = text;
  document.body.appendChild(textField);
  textField.select();
  document.execCommand('copy');
  document.body.removeChild(textField);
}

const inviteBtn = document.getElementById('invite-btn');
const groupId = inviteBtn.dataset.groupId;

// function copyLink() {
//   const url = `http://ec2-3-106-87-11.ap-southeast-2.compute.amazonaws.com:8000/groups/${groupId}/join`;
//   copyToClipboard(url);
//   alert("초대링크가 복사되었습니다.");
// }
function copyLink() {
  const currentDomain = window.location.host;
  const url = `http://${currentDomain}/groups/${groupId}/join`;
  copyToClipboard(url);
  alert("초대링크가 복사되었습니다.");
}
