# 프로젝트 기획

## 프로젝트 개요

| 프로젝트 명 | jelly |
| --- | --- |
| 주제 | 소규모 그룹의 친목 도모 및 추억 공유 커뮤니티 웹사이트 |
| 프로젝트 기간 | 5/22 ~ 6/16 |
| 발표 날짜 | 6/16 |
| 팀명 | 5공주 |

### 프로젝트 툴
- [노션](https://www.notion.so/hg-edu/10-5-6c06557e83784adc912fa3b12a1d42a7)

- [피그잼](https://www.figma.com/file/yIj9mmyghqyUOIEweIpMed/Untitled?type=design&node-id=0-1)

- [피그](https://www.figma.com/file/yIj9mmyghqyUOIEweIpMed/Untitled?type=design&node-id=0-1&t=0oySVFtLVJ5belTV-0)


## 기술 스택
<div align="center">
	<img src="https://img.shields.io/badge/DJANGO-092E20?style=for-the-badge&logo=django&logoColor=white">
	<img src="https://img.shields.io/badge/PYTHON-3776AB?style=for-the-badge&logo=Python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Amazon AWS-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white"/>
  <img src="https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=Ubuntu&logoColor=white"/>
  <img src="https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white"/>
	<br>
  <img src="https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=HTML5&logoColor=white"/>
	<img src="https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=CSS3&logoColor=white"/>
	<img src="https://img.shields.io/badge/JAVASCRIPT-F7DF1E?style=for-the-badge&logo=Javascript&logoColor=white"/>
  <img src="https://img.shields.io/badge/JQUERY-0769AD?style=for-the-badge&logo=JQUERY&logoColor=white"/>
  <img src="https://img.shields.io/badge/Tailwind CSS-06B6D4?style=for-the-badge&logo=Tailwind CSS&logoColor=white"/>
</div>

## 개발 역할 분담

| 이름 | 역할 | 세부 사항 |
| --- | --- |---|
| 조현영 | 조장님, 프론트엔드 개발 | accounts, post detail, vote, group create, navbar, sidebar |
| 최은비 | 프론트엔드 개발 | diary, group_detail, profile |
| 이수정 | 프론트엔드 개발 | index, schedule |
| 하성범 | 백엔드 개발 | accounts, diaries(ckeditor), chat(django-channel, redis), 배포(AWS, ubuntu) |
| 최수현 | 백엔드 개발 | groups(group, post, vote), 배포(AWS, ubuntu) |

## 주제 사전 조사 & 분석

[인스타](https://www.instagram.com/)

[페이스북](https://ko-kr.facebook.com/)

[네이버 밴드](https://band.us/)

[디스코드](https://discord.com/)

## 서비스 주요 기능

<details>
  <summary> 회원관리 </summary>
  <div>
    - 회원가입<br>
    - 로그인<br>
    - 로그아웃<br>
    - 프로필
  </div>
</details>
<br>

<details>
<summary> 그룹 </summary>
<div>
  - 그룹 생성 & 관리(초대, 탈퇴, 방장위임 등)<br>
  - 그룹 레벨(그룹 활동 시 경험치 획득)<br>
  - 게시글(댓글 & 감정표현)<br>
  - 투표
</div>
</details>
<br>

<details>
<summary>채팅</summary>
<div>
  - 각 그룹별 채팅 기능(redis, django-channels사용)
</div>
</details>
<br>

<details>
<summary>다이어리</summary>
<div>
  - 개인 다이어리<br>
  - 그룹에 공유<br>
  - 댓글 & 감정표현<br>
</div>
</details>
<br>

<details>
<summary>스케줄</summary>
<div>
  - 개인 스케줄 관리
  - 그룹 스케줄 관리
</div>
</details>
<br>

## 모델(Model) 설계

![ERD](readme_img/ERD.png)

## 화면(Template) 설계

<details>
  <summary>인덱스</summary>
  <div>
  <img src="readme_img/index.png">
  </div>
</details>

<details>
<summary>회원가입 / 로그인</summary>
<div>
  - 로그인
  <img src="readme_img/login.png">
  - 회원가입
  <img src="readme_img/signup.png">
  - 프로필
  <img src="readme_img/profile.png">
</div>
</details>

<details>
<summary>그룹</summary>
<div>
  - 그룹 가입
  <img src="readme_img/group_join.png">
  - 메인
  <img src="readme_img/group_main.png">
  - 스케줄
  <img src="readme_img/group_schedule.png">
  - 채팅
  <img src="readme_img/chat.png">
  - 앨범
  <img src="readme_img/group_album.png">
  - 그룹 레벨
  <img src="readme_img/group_level.png">
</div>
</details>

<details>
<summary>그룹 게시글 & 투표</summary>
<div>
  - 게시글
  <img src="readme_img/post.png">
  - 참여한 투표
  <img src="readme_img/vote.png">
  - 참여하지 않은 투표
  <img src="readme_img/vote2.png">
</div>
</details>

<details>
<summary>다이어리</summary>
<div>
  - 다이어리 작성
  <img src="readme_img/ckeditor.png">
  - 다이어리 그룹 공유
  <img src="readme_img/diary_share.png">
</div>
</details>
