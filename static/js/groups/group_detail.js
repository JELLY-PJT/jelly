const createBtn = document.getElementById('dropdownDefaultButton')
const dialBtn = document.getElementById('dial-btn')

if (window.scrollY >= 330) {
  dialBtn.classList.remove('hidden')
}

window.addEventListener('scroll', function() {
    if (this.scrollY >= 330) {
    createBtn.style.display = 'none'
    dialBtn.classList.remove('hidden')
  } else {
    createBtn.style.display = 'flex'
    dialBtn.classList.add('hidden')
  }
})

// // owl carousel
// $('.owl-carousel').owlCarousel({
//     loop:false,
//     margin:10,
//     nav:false,
//     responsive:{
//         0:{
//             items:1,
//             slideBy:4,
//             rows:2,
//         },
//         600:{
//             items:2,
//             slideBy:8,
//             rows:2,
//         },
//         1000:{
//             items:4,
//             slideBy:12,
//             rows:2,
//         },
//     }
// })

// // 모달 열기
// $('.img').on('click', function() {
//   var imageUrl = $(this).find('img').attr('src');
//   $('.modal-picture').removeClass('hidden');
//   $('.modal-image').attr('src', imageUrl);
// });
// // 모달 닫기
// $('.modal-picture').on('click', function(event) {
//   // 모달 내부를 클릭한 경우에는 모달이 닫히지 않도록 이벤트 전파 중단
//   if ($(event.target).hasClass('modal-content')) {
//     return;
//   }
//   $('.modal-picture').addClass('hidden');
//   $('.modal-image').attr('src', '');
// });
// // 모달 닫기 버튼 클릭 이벤트
// $('.close-picture').on('click', function() {
//   $('.modal-picture').addClass('hidden');
//   $('.modal-image').attr('src', '');
// });