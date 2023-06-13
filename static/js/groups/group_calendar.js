class CalendarDate {
  constructor(year, month, date) {
    this.year = new Date(year, month, date).getYear();
    this.month = new Date(year, month, date).getMonth();
    this.date = new Date(year, month, date).getDate();
    this.dateCell = undefined;
  }

  Date() {
    return new Date(this.year, this.month, this.date)
  }

  drawDateCell(container, classList) {
    this.dateCell = document.createElement("div");
    this.dateCell.className = classList;
    const square = document.createElement("div");
    square.className = "square";
    const inner = document.createElement("div");
    inner.className = "inner"
    inner.innerHTML = this.date;

    square.appendChild(inner);
    this.dateCell.appendChild(square);
    container.appendChild(this.dateCell);

    this.dateCell.addEventListener('click', (event) => {
      event.preventDefault()
      this.showNoteForDate(noteArea);
    });
  }

  // 노트 표시 함수
  showNoteForDate(noteArea) {
    console.log("showNoteForDate is running!");
    noteArea.innerHTML = "";

    // note Header
    const noteHeader = document.createElement("div");
    noteHeader.className = "note-header";

    const noteHeaderDate = document.createElement("div");
    noteHeaderDate.className = "note-header-date";
    noteHeaderDate.innerHTML = `<div class="square"><div class="inner">${this.date}</div></div>`;

    const scheduleCreateButton = document.createElement("button");

    noteHeader.appendChild(noteHeaderDate);
    noteHeader.appendChild(scheduleCreateButton);

    scheduleCreateButton.outerHTML = `
    <button id="schedule-create-button" class="" data-modal-target="ScheduleCreate-modal" data-modal-toggle="ScheduleCreate-modal">
    <div class="square"><div class="inner">
      <svg class="icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path fill-rule="evenodd" clip-rule="evenodd" d="M12 4C12.5523 4 13 4.44772 13 5V19C13 19.5523 12.5523 20 12 20C11.4477 20 11 19.5523 11 19V5C11 4.44772 11.4477 4 12 4Z"></path>
        <path fill-rule="evenodd" clip-rule="evenodd" d="M4 12C4 11.4477 4.44772 11 5 11H19C19.5523 11 20 11.4477 20 12C20 12.5523 19.5523 13 19 13H5C4.44772 13 4 12.5523 4 12Z"></path>
      </svg>
    </div></div>
    </button>
  `;
    noteArea.appendChild(noteHeader);

    // note content
    const noteContent = document.createElement("div");
    noteContent.className = "note-content";
    this.schedules.forEach(schedule => {
      noteContent.appendChild(schedule.note());
    });
    
    noteArea.appendChild(noteContent);
  }
}

class Schedule {
  constructor(id, calendar, start, end, summary, location, attendee, description) {
    this.id = id;
    this.start = start;
    this.end = end;
    this.calendarId = calendar // 일정 소속 캘린더
    this.summary = summary  // 일정 제목
    this.location = location // 장소
    this.attendee = attendee // 참석자
    this.description = description  // 일정 상세 내용

    this.startDate = new Date(this.start);
    this.endDate = new Date(this.end);

    this.dateCells = [];
    this.dummyDateCells = [];
    this.scheduleBars = [];
  }

  displaySchedule(calendar) {
    // link CalendarDate - Schedule
    this.dateCells = [];
    this.dummyDateCells = [];

    calendar.Dates.forEach(dateItem => {
      dateItem.schedules = [];
      if (this.startDate.getMonth() == dateItem.month) {
        if (this.startDate.getDate() <= dateItem.date && dateItem.date <= this.endDate.getDate()) {
          this.dateCells.push(dateItem);
          dateItem.schedules.push(this)
        }
      }
    });

    // create ScheduleBars
    this.scheduleBars = [];

    this.dateCells.forEach(dateCell => {
      const scheduleBar = document.createElement("div");
      scheduleBar.className = "hidden-schedule-bar";
      scheduleBar.innerHTML = `<p></p>`;
      dateCell.dateCell.appendChild(scheduleBar);
      this.scheduleBars.push(scheduleBar);
    });
    // TODO : 스케쥴 바 알고리즘 재작성.
    // TODO :  make scheduleBar dragable, add drag EventListner, add doubleclick EnvetListner -> modal..
    const firstBarWidth = Math.min(this.dateCells.length, 7 - this.startDate.getDay());
    const lastBarWidth = this.endDate.getDay() + 1;
    this.scheduleBars[0].className = "schedule-bar";
    this.scheduleBars[0].innerHTML = `<p>${this.summary}</p>`;
    this.scheduleBars[0].setAttribute("style", `background-color:var(--color-main-dark);width:calc(var(--date-cell-width)*${firstBarWidth});z-index:9999; font-size:0.3rem;`);

    for (var i = firstBarWidth; i < this.dateCells.length; i += 7) {
      if (i + 7 < this.dateCells.length) {
        this.scheduleBars[i].className = "schedule-bar";
        this.scheduleBars[i].innerHTML = `<p>${this.summary}</p>`;
        this.scheduleBars[i].setAttribute("style", `background-color:var(--color-main-dark);width:calc(var(--date-cell-width)*7);z-index:9999; font-size:0.3rem;`);
      } else {
        this.scheduleBars[i].className = "schedule-bar";
        this.scheduleBars[i].innerHTML = `<p>${this.summary}</p>`;
        this.scheduleBars[i].setAttribute("style", `background-color:var(--color-main-dark);width:calc(var(--date-cell-width)*${lastBarWidth});z-index:9999; font-size:0.3rem;`);
      }
    }
  }

  note() {
    const ScheduleNote = document.createElement("div");
    ScheduleNote.classList = "schedule-note";
    ScheduleNote.innerHTML = `
      <p> ✅ ${this.summary}</p>
      <p>시작 : ${this.startDate.toLocaleString('ko-KR', { dateStyle:'medium', timeStyle:'short', timeZone: 'UTC' })}</p>
      <p>종료 : ${this.endDate.toLocaleString('ko-KR',  { dateStyle:'medium', timeStyle:'short', timeZone: 'UTC' })}</p>
      <p>장소 : ${this.location}</p>
      <p>참석자 : ${this.attendee}</p>
      <p>상세 : ${this.description}</p>`;
    return ScheduleNote
  }
}

class MonthCalendar {
  // constructor
  constructor(year, month) {
    this.year = year;
    this.month = month;

    // 요일 헤더
    this.days = ["일", "월", "화", "수", "목", "금", "토"];

    // 시작 요일, 종료일
    this.monthStartDay = new Date(year, month, 1).getDay(); // Sun Mon Tue Wed Thu Fri Sat : 0 ~ 6
    this.monthEndDate = new Date(year, month + 1, 0).getDate();
    this.nextMonthFirstDay = new Date(year, month + 1, 1).getDay(); // Sun Mon Tue Wed Thu Fri Sat : 0 ~ 6

    this.beforeMonthDates = [];
    for (let day = this.monthStartDay; day > 0; day--) {
      this.beforeMonthDates.push(new CalendarDate(year, month, 1 - day));
    }
    this.Dates = [];
    for (let date = 1; date <= this.monthEndDate; date++) {
      this.Dates.push(new CalendarDate(year, month, date));
    }
    this.afterMonthDates = [];
    for (let day = 0; day + this.nextMonthFirstDay < 7; day++) {
      this.afterMonthDates.push(new CalendarDate(year, month, this.monthEndDate + day + 1));
    }

    this.schedules = [];
    this.domElement = undefined;
  }

}


// 그룹 캘린더를 그려봅시다
const calendarYear = document.getElementById('calendar-year');
const calendarMonth = document.getElementById('calendar-month');
const calendarArea = document.getElementById('calendar-area');
const noteArea = document.getElementById('note-area');
// 현재 날짜 가져오기
const currentDate = new Date();
// 요일 이름
const days = ["일", "월", "화", "수", "목", "금", "토"];

// 달력 생성 함수
const generateCalendar = (year, month = null) => {
  console.log("Calendar is running!");
  console.log(year, month + 1)

  // 이전 달/연도 버튼
  const prevButton = document.createElement("a");
  prevButton.href = "#";
  prevButton.innerHTML = "<";
  prevButton.className = "btn-prev";
  prevButton.addEventListener("click", function () {
    if (month === null) {
      const prevYear = new Date(year, month);
      generateCalendar(prevYear.getFullYear() - 1);
    } else {
      const prevMonth = new Date(year, month - 1);
      generateCalendar(prevMonth.getFullYear(), prevMonth.getMonth());
    }
  });

  // 다음 달/연도 버튼
  const nextButton = document.createElement("a");
  nextButton.href = "#";
  nextButton.innerHTML = ">";
  nextButton.className = "btn-next";
  nextButton.addEventListener("click", function () {
    if (month === null) {
      const prevYear = new Date(year, month);
      generateCalendar(prevYear.getFullYear() + 1);
    } else {
      const nextMonth = new Date(year, month + 1);
      generateCalendar(nextMonth.getFullYear(), nextMonth.getMonth());
    }
  });

  // 연도와 월 표시
  const headerTitle = document.createElement("div");
  headerTitle.innerHTML = month === null ? year + "년 " : year + "년 " + (month + 1) + "월";
  headerTitle.className = "calendar-title";
  headerTitle.addEventListener("click", function () {
    generateCalendar(year);
  });

  // 이전 달력 삭제
  while (calendarArea.firstChild) {
    calendarArea.firstChild.remove();
  }

  // 달력에 추가

  const calendarHeader = document.createElement("div");
  calendarHeader.classList = "calendar-header"
  calendarHeader.appendChild(prevButton);
  calendarHeader.appendChild(headerTitle);
  calendarHeader.appendChild(nextButton);
  calendarArea.appendChild(calendarHeader);
  if (month === null) {
    // 연도 달력
    generateYearCalendar(calendarArea, year);
  } else {
    // 월 달력
    return generateMonthCalendar(calendarArea, year, month);
  }
}

// 연도별 달력
const generateYearCalendar = (calendarArea, year) => {
  const monthContainer = document.createElement("div");
  monthContainer.className = "calendar-months";
  for (let i = 0; i < 12; i++) {
    const monthCell = document.createElement("div");
    monthCell.innerHTML = i + 1 + "월";
    monthCell.className = "calendar-month";
    monthCell.addEventListener("click", function () {
      generateCalendar(year, i);
    });
    monthContainer.appendChild(monthCell);
  }
  calendarArea.appendChild(monthContainer);
}

// 월별 달력
const generateMonthCalendar = (calendarArea, year, month) => {
  console.log('generate Month Calendar');
  const calendar = new MonthCalendar(year, month);

  // 요일 헤더 생성
  console.log('create Header');
  const daysRow = document.createElement("div");
  daysRow.className = "day-row"; // grid-row repeat(7, 1fr)
  days.forEach(day => {
    const dayCell = document.createElement("div");
    dayCell.innerHTML = `<div class="square"><div class="inner"><div class="calendar-day">${day}</div></div></div>`;
    daysRow.appendChild(dayCell);
  });

  // 날짜 채우기
  console.log('create DateCells');
  const dateContainer = document.createElement("div");
  dateContainer.className = "date-container"; // grid-row repeat(7, 1fr)
  calendar.beforeMonthDates.forEach(date => {
    date.drawDateCell(dateContainer, 'calendar-date other-month');
  });
  calendar.Dates.forEach(date => {
    date.drawDateCell(dateContainer, 'calendar-date');        
  });
  calendar.afterMonthDates.forEach(date => {
    date.drawDateCell(dateContainer, 'calendar-date other-month');
  });

  calendarArea.appendChild(daysRow);
  calendarArea.appendChild(dateContainer);
  return calendar;
}

// 스케쥴 가져오기 함수 
async function fetchAndDisplaySchedules() {
  try {
    // 현재 날짜로 달력 생성
    const calendar = generateCalendar(currentDate.getFullYear(), currentDate.getMonth());

    axios({
      method: 'get',
      url: `calendars/schedules/?year=${calendar.year}&month=${calendar.month + 1}`,
      responseType: 'json',
    })
      .then(function (response) {

        console.log('response');
        console.log(response.data);

        response.data.forEach(item => {
          console.log('item detail');
          calendar.schedules.push(new Schedule(
            item.id,
            item.calendar,
            item.start,
            item.end,
            item.summary,
            item.location,
            item.attendee,
            item.description
          ));
        });
      })
      .then(function () {
        console.log('fetch Schedules');
        console.log(calendar.schedules);

        console.log('create ScheduleBars');
        calendar.schedules.forEach(schedule => {
        schedule.displaySchedule(calendar);
        
        calendar.Dates.forEach(date => {
          date.dateCell.addEventListener('click', (event) => {
            event.preventDefault();
            date.showNoteForDate(noteArea);
          });
        });
        // 현재 날짜의 노트 표시
        calendar.Dates[currentDate.getDate()-1].showNoteForDate(noteArea);
      });
    });
  } catch (error) {
    console.error(error);
  };
}

// 스케쥴 가져오기
fetchAndDisplaySchedules();
