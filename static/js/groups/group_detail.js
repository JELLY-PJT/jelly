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

// 해당 사진이 포함된 게시글로 이동
const albumImages = document.querySelectorAll('.album-img')
const prevBtn = document.querySelector('.album-left')

if (albumImages) {
  albumImages.forEach(function(img, index) {
    img.addEventListener('click', function() {
      addImage(img)
    })
    prevBtn.addEventListener('click', function() {
      console.log(albumImages[index-1])
      addImage(albumImages[index-1])
    })
  })
}

function addImage(img) {
  let imageUrl = img.children[0].getAttribute('src')
  let postId = img.getAttribute('data-post-id')
  document.querySelector('.modal-link').setAttribute('href', `./posts/${postId}`)
  document.querySelector('.modal-image').setAttribute('src', `${imageUrl}`)
}