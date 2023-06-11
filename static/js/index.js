// 검색창에 text입력 시 바로 검색결과 나오는 기능
const searchInput = document.getElementById('search-input')
const GroupButtonGrid = document.getElementById('group-buttons-grid')
// const searchResults = document.getElementById('search-results')
// const moviesDiv = document.getElementById('selected-list')
// const selectedList = []
// const moviesInput = document.getElementById('movies-input')

searchInput.addEventListener('keydown input', async (event) => {
  const query = searchInput.value
  if (query) {
    try {
      axios({
        method: 'get',
        url: `./search?q=${query}`,
        responseType: 'json',
      })
      .then(function (response) {
        GroupButtonGrid.innerHTML=""
        response.data.forEach(item => {
          GroupButtonGrid.appendChild(drawButton(item.id, item.name, item.thumbnail));
        });
      });
    } catch (error) {
      console.error(error)
    }
  } else {
    // searchResults.innerHTML = '';
  }
})
// 버튼 그리기
function drawButton(id, name, thumbnail){
  const btnTag = document.createElement('button');
  btnTag.classList.add('item', 'button');
  btnTag.innerHTML=`<a href="./${id}"><div class="square"><div class="inner"><div class="group-button-thumbnail"><img src="${thumbnail}" alt=""></div><div class="group-button-name"><span>${name}</span></div></div></div></a>`;
  return btnTag;
}

function handleLoad(){
  try {
    axios({
      method: 'get',
      url: `./search?q= `,
      responseType: 'json',
    })
    .then(function (response) {
      GroupButtonGrid.innerHTML=""
      response.data.forEach(item => {
        GroupButtonGrid.appendChild(drawButton(item.id, item.name, item.thumbnail));
      });
    });
  } catch (error) {
    console.error(error)
  }
}

// 화면 로드 시 호출
window.addEventListener('load', handleLoad);
// 리사이징 이벤트 시 호출
// window.addEventListener('resize', handleResize);