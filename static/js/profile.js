// 스크롤을 올렸을 때 글작성 버튼이 아래에 나타나는 코드
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

// 탭 이동 관련 코드
const postTabBtn = document.getElementById('post-tab')
const shareTabBtn = document.getElementById('share-tab')
const calendarTabBtn = document.getElementById('calendar-tab')
const postTab = document.getElementById('post')
const shareTab = document.getElementById('share')
const calendarTab = document.getElementById('calendar')
const nowUrl = window.location.href

if ( nowUrl.includes('share') ) {
  postTab.classList.add('hidden')
  shareTab.classList.remove('hidden')
  calendarTab.classList.add('hidden')
  postTabBtn.ariaSelected = false
  shareTabBtn.ariaSelected = true
  calendarTabBtn.ariaSelected = false
} else if ( nowUrl.includes('calendar') ) {
  postTab.classList.add('hidden')
  shareTab.classList.add('hidden')
  calendarTab.classList.remove('hidden')
  postTabBtn.ariaSelected = false
  shareTabBtn.ariaSelected = false
  calendarTabBtn.ariaSelected = true
} else {
  postTab.classList.remove('hidden')
  shareTab.classList.add('hidden')
  calendarTab.classList.add('hidden')
  postTabBtn.ariaSelected = true
  shareTabBtn.ariaSelected = false
  calendarTabBtn.ariaSelected = false
}


document.querySelectorAll('.tab-btn').forEach((btn) => {
  btn.addEventListener('click', function(event) {
    currentTab = event.target.getAttribute('data-tab')
    const user = event.target.getAttribute('data-user')    
    
    if (currentTab == 'post') {
      if (nowUrl.includes('share')) {
        history.pushState(null, null, nowUrl.replace('share', 'post')) 
      } else if (nowUrl.includes('calendar')) {
        history.pushState(null, null, nowUrl.replace('calendar', 'post')) 
      } else {
        history.pushState(null, null, 'post')
      }
    
      postTabBtn.ariaSelected = true
      shareTabBtn.ariaSelected = false
      calendarTabBtn.ariaSelected = false
      postTab.classList.remove('hidden')
      shareTab.classList.add('hidden')
      calendarTab.classList.add('hidden')
    } else if (currentTab == 'share') {
      if (nowUrl.includes('post')) {
        history.pushState(null, null, nowUrl.replace('post', 'share')) 
      } else if (nowUrl.includes('calendar')) {
        history.pushState(null, null, nowUrl.replace('calendar', 'share')) 
      } else {
        history.pushState(null, null, 'share')
      }
      postTabBtn.ariaSelected = false
      shareTabBtn.ariaSelected = true
      calendarTabBtn.ariaSelected = false
      postTab.classList.add('hidden')
      shareTab.classList.remove('hidden')
      calendarTab.classList.add('hidden')
    } else {
      if (nowUrl.includes('share')) {
        history.pushState(null, null, nowUrl.replace('share', 'calendar')) 
      } else if (nowUrl.includes('calendar')) {
        history.pushState(null, null, nowUrl.replace('post', 'calendar')) 
      } else {
        history.pushState(null, null, 'calendar')  
      }
    
      postTabBtn.ariaSelected = false
      shareTabBtn.ariaSelected = false
      calendarTabBtn.ariaSelected = true
      postTab.classList.add('hidden')
      shareTab.classList.add('hidden')
      calendarTab.classList.remove('hidden')
    }
  })
})