const selectThumbnailBtn = document.getElementById('select-thumbnail-btn')
const thumbnailInput = document.getElementById('thumbnail_input')
let images = null
let selectedImage = null

// '썸네일 선택하기' 버튼 클릭 시 이미지 선택 기능 활성화
selectThumbnailBtn.addEventListener('click', function() {
  images = document.querySelectorAll('.ck-editor__main img')
  // 이미지 클릭 이벤트 핸들러 등록
  for (var i = 0; i < images.length; i++) {
    images[i].addEventListener('click', selectImageOnce)
  }
})

const badge = document.querySelector('.thumbnail-btn')

// 이미지 클릭 시 선택 처리
function selectImageOnce() {
  if (selectedImage) {
    selectedImage.removeAttribute('id')
    selectedImage.classList.remove('thumbnail-border')
    badge.style.display = 'none'
  }

  this.id = 'thumbnail'
  selectedImage = this
  thumbnailInput.setAttribute('value', `${this.src}`)
  
  // 썸네일 뱃지 표시
  badge.style.display = 'block'
  // 썸네일 뱃지 위치 조정
  badge.style.top = this.getBoundingClientRect().top + window.scrollY + 10 + 'px'
  badge.style.right = this.getBoundingClientRect().left - 120 + 'px'
  // border
  selectedImage.classList.add('thumbnail-border')

  for (var i = 0; i < images.length; i++) {
    images[i].removeEventListener('click', selectImageOnce)
  }
}