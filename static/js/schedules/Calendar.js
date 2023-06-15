
const days = ["일", "월", "화", "수", "목", "금", "토"];

export class CalendarDate {
  constructor(year, month, date) {
    this.year = new Date(year, month, date).getYear();
    this.month = new Date(year, month, date).getMonth();
    this.date = new Date(year, month, date).getDate();
  }

  Date() {
    return new Date(this.year, this.month, this.date)
  }

  drawDateCell(container, classList, noteArea) {
    if (this.dateCell) {
          this.dateCell.innerHTML="";
    } else {
      this.dateCell = document.createElement("div");
      this.dateCell.className = classList
    }
    const square = document.createElement("div");
    square.className = "square";
    const inner = document.createElement("div");
    inner.className = "inner"
    inner.innerHTML = this.date;
    const gridColumn = document.createElement("div");
    gridColumn.className = "schedule-grid"
    const gridCell = document.createElement("div");
    gridCell.className = "schedule-grid-cell"


    gridColumn.appendChild(gridCell.cloneNode(true));
    gridColumn.appendChild(gridCell.cloneNode(true));
    gridColumn.appendChild(gridCell.cloneNode(true));

    square.appendChild(inner);
    this.dateCell.appendChild(square);
    this.dateCell.appendChild(gridColumn);
    container.appendChild(this.dateCell);

    this.dateCell.children[0].addEventListener('click', (event) => {
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

    const headerDateArea = document.createElement("div");
    headerDateArea.classList = "header-date-area";
    const headerCreateButtonArea = document.createElement("div");
    headerCreateButtonArea.classList = "header-button-area";
    const headerFormArea = document.createElement("div");
    headerFormArea.classList = "header-form-area";

    const noteHeaderDate = document.createElement("div");
    noteHeaderDate.className = "note-header-date";
    noteHeaderDate.textContent = `${this.date}`;

    const scheduleCreateButton = document.createElement("button");
    scheduleCreateButton.setAttribute('id', "create-schedule-button");
    scheduleCreateButton.setAttribute('name', "create-schedule-button");
    scheduleCreateButton.setAttribute('form', "create-schedule-form");
    scheduleCreateButton.innerHTML = `
    <div class="square"><div class="inner">
      <svg class="icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path fill-rule="evenodd" clip-rule="evenodd" d="M12 4C12.5523 4 13 4.44772 13 5V19C13 19.5523 12.5523 20 12 20C11.4477 20 11 19.5523 11 19V5C11 4.44772 11.4477 4 12 4Z"></path>
        <path fill-rule="evenodd" clip-rule="evenodd" d="M4 12C4 11.4477 4.44772 11 5 11H19C19.5523 11 20 11.4477 20 12C20 12.5523 19.5523 13 19 13H5C4.44772 13 4 12.5523 4 12Z"></path>
      </svg>
    </div></div>`;

    const form = document.createElement("form");
    form.setAttribute('id', `create-schedule-form`);
    form.setAttribute('action', "#");
    form.setAttribute('data-calendar-id', `${this.id}`);

    const formInputArea = document.createElement("div");
    formInputArea.classList = "create-form-input-area";
    formInputArea.innerHTML = `
  <div class="form-group"><label>Start</label><div><input name="start" type="datetime-local" value="" ></div></div>
  <div class="form-group"><label>End</label><div ><input name="end" type="datetime-local" value="" ></div></div>
  <div class="form-group"><label>Summary</label><div ><input name="summary" type="text" value="" ></div></div>
  <div class="form-group"><label>Location</label><div ><input name="location" type="text" value="" ></div></div>
  <div class="form-group"><label>Description</label><div ><input name="description" type="text" value="" ></div></div>`;
    
    const formSCButtonArea = document.createElement("div");
    formSCButtonArea.classList = "create-form-button-area";
    
    const saveButton = document.createElement("button");
    saveButton.setAttribute('name', `post-schedule-button`);
    saveButton.setAttribute('form', `create-schedule-form`);
    saveButton.setAttribute('type', 'button');
    saveButton.textContent = '저장';
    
    const cancelButton = document.createElement("button");
    cancelButton.setAttribute('name', `cancel-create-schedule-button`);
    cancelButton.setAttribute('form', `create-schedule-form`);
    cancelButton.setAttribute('type', 'button');
    cancelButton.textContent = '취소';

    formSCButtonArea.appendChild(saveButton);
    formSCButtonArea.appendChild(cancelButton);

    form.appendChild(formInputArea);
    form.appendChild(formSCButtonArea);

    headerDateArea.appendChild(noteHeaderDate);
    headerCreateButtonArea.appendChild(scheduleCreateButton);
    headerFormArea.appendChild(form);
    
    noteHeader.appendChild(headerDateArea);
    noteHeader.appendChild(headerCreateButtonArea);
    noteHeader.appendChild(headerFormArea);
    
    noteArea.appendChild(noteHeader);

    // note content
    const noteContent = document.createElement("div");
    noteContent.className = "note-content";
    if (this.schedules) {
      this.schedules.forEach(schedule => {
        const ScheduleNote = schedule.note();
        noteContent.appendChild(ScheduleNote);
      });
    }

    noteArea.appendChild(noteContent);
    this.createEventListeners(noteArea);
  }

  createEventListeners(noteArea) {

    //create form 표시
    noteArea.querySelector('#create-schedule-button').addEventListener('click', function (event) {
      event.preventDefault();
      document.querySelector(".header-button-area").style.display = 'none';
      document.querySelector(".header-form-area").style.display = 'block';
    });

    noteArea.querySelector('#create-schedule-form').querySelectorAll('button').forEach(button => {
      switch (button.getAttribute('name')) {
        //create
        case 'post-schedule-button':

          button.addEventListener('click', function (event) {
            event.preventDefault();
            const formId = button.getAttribute('form');
            createSchedule(formId);
          });

          break;
        // cancel create
        case 'cancel-create-schedule-button':
          button.addEventListener('click', function (event) {
            event.preventDefault();
            document.querySelector(".header-button-area").style.display = 'block';
            document.querySelector(".header-form-area").style.display = 'none';
          });
          break;
        default:
          // 기본 동작 없음;
          break;
      }
  })
    
    noteArea.querySelectorAll('.schedule-note').forEach(scheduleNote => {
      scheduleNote.querySelectorAll("button").forEach(button => {
      switch (button.getAttribute('name')) {
        //update form 표시
        case 'update-schedule-button':
          button.addEventListener('click', function (event) {
            event.preventDefault();
            const form = document.getElementById(button.getAttribute('form'));
            form.querySelector(".form-readonly-area").style.display = 'none';
            form.querySelector(".form-readonly-button-area").style.display = 'none';
            form.querySelector(".form-input-area").style.display = 'block';
            form.querySelector(".form-input-button-area").style.display = 'block';
          });
          break;
        //delete
        case 'delete-schedule-button':
          // button.addEventListener('click', deleteSchedule(calendar));
          button.addEventListener('click', function (event) {
            event.preventDefault();
            const formId = button.getAttribute('form');
            deleteSchedule(formId)
          });
          break;
          
        //update
        case 'post-update-schedule-button':
          // button.addEventListener('click', updateSchedule(calendar));
          button.addEventListener('click', function (event) {
            event.preventDefault();
            const formId = button.getAttribute('form');
            updateSchedule(formId)
          });
          break;

        //update 취소
        case 'cancel-update-schedule-button':
          button.addEventListener('click', function (event) {
            event.preventDefault();
            const form = button.getAttribute('form');
            form.querySelector(".form-readonly-area").style.display = 'block';
            form.querySelector(".form-readonly-button-area").style.display = 'block';
            form.querySelector(".form-input-area").style.display = 'none';
            form.querySelector(".form-input-button-area").style.display = 'none';
          });
          break;

        default:
          // 기본 동작 없음;
          break;
      }
      })
    })
  }
}

export class MonthCalendar {
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
    this.calendarStartDate = new Date(year, month, 1 - this.beforeMonthDates.length);

    this.Dates = [];
    for (let date = 0; date < this.monthEndDate; date++) {
      this.Dates.push(new CalendarDate(year, month, date + 1));
    }
    this.afterMonthDates = [];
    for (let day = 0; day + this.nextMonthFirstDay < 7; day++) {
      this.afterMonthDates.push(new CalendarDate(year, month, this.monthEndDate + day + 1));
    }
    this.calendarEndDate = new Date(year, month + 1, this.afterMonthDates.length);

  }

  getGridCell(date, row) {
    return this.Dates[date - 1].dateCell.children[1].children[row - 1];
  }

  checkGridStatus(schedule) {
    var r = [0, 0, 0]
    for (var i = schedule.startDate.getDate() - 1; i < schedule.scheduleBarWidth + schedule.startDate.getDate() - 1; i++) {
      for (var j = 0; j < r.length; j++) {
        r[j] = r[j] + this.gridStatus[i][j];
      }
    }
    for (var j = 0; j < r.length; j++) {
      if (r[j] == 0) {
        for (var i = schedule.startDate.getDate() - 1; i < schedule.scheduleBarWidth + schedule.startDate.getDate() - 1; i++) {
          this.gridStatus[i][j] = 1;
        }
        return j + 1
      }
    }
    return false;
  }
}

// 달력 생성 함수
export function generateCalendar(calendarArea, noteArea, year, month = null) {
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
      generateCalendar(calendarArea, noteArea, prevYear.getFullYear() - 1);
    } else {
      const prevMonth = new Date(year, month - 1);
      generateCalendar(calendarArea, noteArea, prevMonth.getFullYear(), prevMonth.getMonth());
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
      generateCalendar(calendarArea, noteArea, prevYear.getFullYear() + 1);
    } else {
      const nextMonth = new Date(year, month + 1);
      generateCalendar(calendarArea, noteArea, nextMonth.getFullYear(), nextMonth.getMonth());
    }
  });

  // 연도와 월 표시
  const headerTitle = document.createElement("div");
  headerTitle.innerHTML = month === null ? year + "년 " : year + "년 " + (month + 1) + "월";
  headerTitle.className = "calendar-title";
  headerTitle.addEventListener("click", function () {
    generateCalendar(calendarArea, noteArea, year);
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
    generateYearCalendar(calendarArea, noteArea, year);
  } else {
    // 월 달력
    return generateMonthCalendar(calendarArea, noteArea, year, month);
  }
}

// 연도별 달력
function generateYearCalendar(calendarArea, noteArea, year) {
  const monthContainer = document.createElement("div");
  monthContainer.className = "calendar-months";
  for (let i = 0; i < 12; i++) {
    const monthCell = document.createElement("div");
    monthCell.innerHTML = i + 1 + "월";
    monthCell.className = "calendar-month";
    monthCell.addEventListener("click", function () {
      generateCalendar(calendarArea, noteArea, year, i);
    });
    monthContainer.appendChild(monthCell);
  }
  calendarArea.appendChild(monthContainer);
}

// 월별 달력
function generateMonthCalendar(calendarArea, noteArea, year, month) {
  const calendar = new MonthCalendar(year, month);

  // 요일 헤더 생성
  const daysRow = document.createElement("div");
  daysRow.className = "day-row"; // grid-row repeat(7, 1fr)
  days.forEach(day => {
    const dayCell = document.createElement("div");
    dayCell.innerHTML = `<div class="square"><div class="inner"><div class="calendar-day">${day}</div></div></div>`;
    daysRow.appendChild(dayCell);
  });

  // 날짜 채우기
  const dateContainer = document.createElement("div");
  dateContainer.className = "date-container"; // grid-row repeat(7, 1fr)

  calendar.beforeMonthDates.forEach(date => {
    date.drawDateCell(dateContainer, 'calendar-date other-month', noteArea);
  });
  calendar.Dates.forEach(date => {
    date.drawDateCell(dateContainer, 'calendar-date', noteArea);
  });
  calendar.afterMonthDates.forEach(date => {
    date.drawDateCell(dateContainer, 'calendar-date other-month', noteArea);
  });

  calendarArea.appendChild(daysRow);
  calendarArea.appendChild(dateContainer);

  return calendar;
}
