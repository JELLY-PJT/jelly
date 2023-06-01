// 그룹으로 공유하기 위한 url 생성
const groupSelect = document.getElementById('group-select')
const shareForm = document.getElementById('share-form')
const diaryPk = shareForm.dataset.diaryId
  
groupSelect.addEventListener('change', function() {
  const selectedGroupPk = groupSelect.value
  const shareUrl = "/diaries/" + selectedGroupPk + "/" + diaryPk + "/share/"
  shareForm.action = selectedGroupPk ? shareUrl : ''
})

