class Schedule {
  constructor(id, calendar, start, end, summary, location, description) {
    this.id = id;
    this.start = start;
    this.end = end;
    this.calendarId = calendar // 일정 소속 캘린더
    this.summary = summary  // 일정 제목
    this.location = location // 장소
    this.description = description  // 일정 상세 내용

    this.startDate = new Date(this.start);
    this.startDate_Date = new Date(this.startDate.toDateString())
    this.endDate = new Date(this.end);
    this.endDate_Date = new Date(this.endDate.toDateString())
  }
  createScheduleBars(calendar) {
    console.log(this.calendarId);
    // console.log("create schedule bar");
    // create ScheduleBars
    this.scheduleBars = [];
    const monthStart = new Date(calendar.year, calendar.month, 1)
    const monthEnd = new Date(calendar.year, calendar.month + 1, 0)
    this.barStart = this.startDate
    this.barEnd = this.endDate
    if (this.startDate < monthStart) {
      this.barStart = calendar.monthStart
    }
    if (monthEnd < this.endDate) {
      this.barEnd = monthEnd
    }
    const barStartDate = parseInt(this.barStart.getDate());
    const barEndDate = parseInt(this.barEnd.getDate());
    this.scheduleBarWidth = 1 + barEndDate - barStartDate;

    if (this.startDate.getMonth() == calendar.month) {
      for (var i = barStartDate; i < barEndDate + 1; i++) {
        if (!calendar.Dates[i - 1].schedules) {
          calendar.Dates[i - 1].schedules = [];
        }
        calendar.Dates[i - 1].schedules.push(this);
      }
    }
    const scheduleBarBody = document.createElement("div");
    scheduleBarBody.className = "schedule-bar";
    scheduleBarBody.innerHTML = `<p>${this.summary}</p>`;

    // console.log(this)
    // console.log(`start: ${barStartDate}, end: ${barEndDate}`)
    var i = barStartDate
    while (i <= barEndDate) {
      // console.log("new schedule bar")
      if (i == barStartDate) {
        const scheduleBar = { body: scheduleBarBody.cloneNode(true) }
        // if (barStartDate == 1) {
        //   scheduleBar['width'] = Math.min(this.scheduleBarWidth, 7-calendar.monthStartDay)
        // } else {
        //   scheduleBar['width'] = Math.min(this.scheduleBarWidth, 7-this.startDate.getDay())
        // }
        scheduleBar['width'] = Math.min(this.scheduleBarWidth, 7 - this.barStart.getDay())
        console.log(`userCalendarId: ${userCalendarId}`)
        console.log(`this.calendarId: ${this.calendarId}` )
        scheduleBar['body'].setAttribute(
            "style",
            `width:calc(var(--date-cell-width) * ${scheduleBar['width']} - 1px);
            max-width:calc(var(--date-cell-max-width) * ${scheduleBar['width']} - 1px);
            background-color:var(--color-id-${CalendarDict[this.calendarId]['color']});`
          );
        // console.log(`start: ${i}, width:${scheduleBar['width']}`)
        i += scheduleBar['width']
        this.scheduleBars.push(scheduleBar);
      } else if (i + 7 < barEndDate) {
        const scheduleBar = { body: scheduleBarBody.cloneNode(true), width: 7, }
        scheduleBar['body'].setAttribute(
          "style",
          `width:calc(var(--date-cell-width) * ${scheduleBar['width']} - 1px);
          max-width:calc(var(--date-cell-max-width) * ${scheduleBar['width']} - 1px);
          background-color:var(--color-id-${CalendarDict[this.calendarId]['color']});`
        );
        // console.log(`start: ${i}, width:${scheduleBar['width']}`)
        i += scheduleBar['width']
        this.scheduleBars.push(scheduleBar);
      } else {
        const scheduleBar = { body: scheduleBarBody.cloneNode(true), width: 1 + barEndDate - i }
        scheduleBar['body'].setAttribute(
          "style",
          `width:calc(var(--date-cell-width) * ${scheduleBar['width']} - 1px);
          max-width:calc(var(--date-cell-max-width) * ${scheduleBar['width']} - 1px);
          background-color:var(--color-id-${CalendarDict[this.calendarId]['color']});`
        );
        // console.log(`start: ${i}, width:${scheduleBar['width']}`)
        i += scheduleBar['width']
        this.scheduleBars.push(scheduleBar);
      }
    }

    // console.log(this)
    // console.log(this.barStart)
    // console.log(this.barEnd)
    // console.log(this.scheduleBarWidth)
    // console.log("schedule Bars")
    // console.log(this.scheduleBars)
    this.displayScheduleBars(calendar);
  }
  displayScheduleBars(calendar) {
    // console.log("displayScheduleBars");
    var r = calendar.checkGridStatus(this);
    if (r) {
      var i = this.barStart.getDate();
      this.scheduleBars.forEach(scheduleBar => {
        if (i < parseInt(this.barEnd.getDate()) + 1) {
          // console.log(i-1)
          // console.log(r)
          calendar.getGridCell(i, r).appendChild(scheduleBar['body']);
          i += scheduleBar['width'];
        }
      });
    }
  }
  // TODO :  make scheduleBar dragable, add drag EventListner, add doubleclick EnvetListner -> modal..
  note() {
    const ScheduleNote = document.createElement("div");
    ScheduleNote.classList = "schedule-note";
    const form = document.createElement("form");
    form.classList = "schedule-form";
    form.setAttribute('id', `schedule-form-${this.id}`);
    form.setAttribute('action', "#");
    form.setAttribute('data-schedule-id', `${this.id}`);
    const formReadonlyArea = document.createElement("div");
    formReadonlyArea.classList = "form-readonly-area";
    formReadonlyArea.innerHTML = `
    <div class="form-group"><label>Start</label><div><input name="_start" type="datetime-local" value="${this.start.toString().slice(0, 16)}" readonly></div></div>
    <div class="form-group"><label>End</label><div ><input name="_end" type="datetime-local" value="${this.end.toString().slice(0, 16)}" readonly></div></div>
    <div class="form-group"><label>Summary</label><div ><input name="_summary" type="text" value="${this.summary}" readonly></div></div>
    <div class="form-group"><label>Location</label><div ><input name="_location" type="text" value="${this.location}" readonly></div></div>
    <div class="form-group"><label>Description</label><div ><input name="_description" type="text" value="${this.description}" readonly></div></div>`;
    const formUDButtonArea = document.createElement("div");
    formUDButtonArea.classList = "form-readonly-button-area";
    const updateButton = document.createElement("button");
    updateButton.setAttribute('name', `update-schedule-button`);
    updateButton.setAttribute('form', `schedule-form-${this.id}`);
    updateButton.setAttribute('type', 'button');
    updateButton.textContent = '수정';
    const deleteButton = document.createElement("button");
    deleteButton.setAttribute('name', `delete-schedule-button`);
    deleteButton.setAttribute('form', `schedule-form-${this.id}`);
    deleteButton.setAttribute('type', 'button');
    deleteButton.textContent = '삭제';

    const formInputArea = document.createElement("div");
    formInputArea.classList = "form-input-area";
    formInputArea.innerHTML = `
    <div class="form-group"><label>Start</label><div><input name="start" type="datetime-local" value="${this.start.toString().slice(0, 16)}" ></div></div>
    <div class="form-group"><label>End</label><div ><input name="end" type="datetime-local" value="${this.end.toString().slice(0, 16)}" ></div></div>
    <div class="form-group"><label>Summary</label><div ><input name="summary" type="text" value="${this.summary}" ></div></div>
    <div class="form-group"><label>Location</label><div ><input name="location" type="text" value="${this.location}" ></div></div>
    <div class="form-group"><label>Description</label><div ><input name="description" type="text" value="${this.description}" ></div></div>`;
    const formSCButtonArea = document.createElement("div");
    formSCButtonArea.classList = "form-input-button-area";
    const saveButton = document.createElement("button");
    saveButton.setAttribute('name', `post-update-schedule-button`);
    saveButton.setAttribute('form', `schedule-form-${this.id}`);
    saveButton.setAttribute('type', 'button');
    saveButton.textContent = '저장';
    const cancelButton = document.createElement("button");
    cancelButton.setAttribute('name', `cancel-update-schedule-button`);
    cancelButton.setAttribute('form', `schedule-form-${this.id}`);
    cancelButton.setAttribute('type', 'button');
    cancelButton.textContent = '취소';

    formUDButtonArea.appendChild(updateButton);
    formUDButtonArea.appendChild(deleteButton);
    formSCButtonArea.appendChild(saveButton);
    formSCButtonArea.appendChild(cancelButton);

    form.appendChild(formReadonlyArea);
    form.appendChild(formUDButtonArea);
    form.appendChild(formInputArea);
    form.appendChild(formSCButtonArea);

    ScheduleNote.appendChild(form);

    return ScheduleNote
  }
}
class CalendarDate {
  constructor(year, month, date) {
    this.year = new Date(year, month, date).getYear();
    this.month = new Date(year, month, date).getMonth();
    this.date = new Date(year, month, date).getDate();
  }
  Date() {
    return new Date(this.year, this.month, this.date)
  }

  drawDateCell(container, classList) {
    if (this.dateCell) {
      this.dateCell.innerHTML = "";
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
      this.showNoteForDate();
    });
  }

  cleanDateCell() {
    const gridCell = document.createElement("div");
    gridCell.className = "schedule-grid-cell"
    const gridColumn = this.dateCell.children[1];

    gridColumn.innerHTML = "";

    gridColumn.appendChild(gridCell.cloneNode(true));
    gridColumn.appendChild(gridCell.cloneNode(true));
    gridColumn.appendChild(gridCell.cloneNode(true));

    if (this.schedules) {
      this.schedules = new Array();
    }

  }
  // 노트 표시 함수
  showNoteForDate() {
    // console.log("showNoteForDate is running!");

    // note Area 초기화
    const noteArea = document.getElementById('note-area');
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

    const formInputArea = document.createElement("div");
    formInputArea.classList = "create-form-input-area";

    var index = 1
    var html = `<select name="calendar" required=""><option value="" selected="">---------</option>`
    for (var key in CalendarDict) {
      if (CalendarDict.hasOwnProperty(key)) {
        var value = CalendarDict[key]['name'];
        html += `<option value="${index}">${value}의  캘린더</option>`;
        index += 1
      }
    }
    html += `</select></div></div>`
    console.log(html); 


    formInputArea.innerHTML = `
  <div class="form-group"><label>Start</label><div><input name="start" type="datetime-local" value="" ></div></div>
  <div class="form-group"><label>End</label><div ><input name="end" type="datetime-local" value="" ></div></div>
  <div class="form-group"><label>Summary</label><div ><input name="summary" type="text" value="" ></div></div>
  <div class="form-group"><label>Location</label><div ><input name="location" type="text" value="" ></div></div>
  <div class="form-group"><label>Description</label><div ><input name="description" type="text" value="" ></div></div>
  <div class="form-group"><label>Calendar</label><div>${html}`;


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
    this.createEventListeners();
  }

  createEventListeners() {
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
            const form = document.getElementById(button.getAttribute('form'));
            createSchedule(form)
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
              const form = document.getElementById(button.getAttribute('form'));
              deleteSchedule(form)
            });
            break;

          //update
          case 'post-update-schedule-button':
            // button.addEventListener('click', updateSchedule(calendar));
            button.addEventListener('click', function (event) {
              event.preventDefault();
              const form = document.getElementById(button.getAttribute('form'));
              updateSchedule(form)
            });
            break;

          //update 취소
          case 'cancel-update-schedule-button':
            button.addEventListener('click', function (event) {
              event.preventDefault();
              const form = document.getElementById(button.getAttribute('form'));
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
class MonthCalendar {
  // constructor
  constructor(year, month) {
    this.year = year;
    this.month = month;

    // 요일 헤더
    this.days = ["일", "월", "화", "수", "목", "금", "토"];

    // 시작 요일, 종료일
    this.monthStart = new Date(year, month, 1);
    this.monthEnd = new Date(year, month + 1, 0);
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
  cleanCalendar() {
    // clean date cell
    this.Dates.forEach(Date => {
      Date.cleanDateCell()
    })
    // clean grid status
    this.gridStatus = [];
    for (var i = 0; i < this.monthEndDate; i++) {
      this.gridStatus.push([0, 0, 0]);
    }
  }
  getGridCell(date, row) {
    // console.log(this.Dates[date].dateCell.children[1])
    return this.Dates[date - 1].dateCell.children[1].children[row - 1];
  }
  checkGridStatus(schedule) {
    if (!this.gridStatus) {
      this.gridStatus = [];
      for (var i = 0; i < this.monthEndDate; i++) {
        this.gridStatus.push([0, 0, 0]);
      }
    }

    var r = [0, 0, 0]
    for (var i = schedule.startDate.getDate() - 1; i < Math.min(schedule.scheduleBarWidth + schedule.startDate.getDate() - 1, this.monthEndDate); i++) {
      for (var j = 0; j < r.length; j++) {
        r[j] = r[j] + this.gridStatus[i][j];
      }
    }
    for (var j = 0; j < r.length; j++) {
      if (r[j] == 0) {
        for (var i = schedule.startDate.getDate() - 1; i < Math.min(schedule.scheduleBarWidth + schedule.startDate.getDate() - 1, this.monthEndDate); i++) {
          this.gridStatus[i][j] = 1;
        }
        return j + 1
      }
    }
    return false;
  }
}
// 달력 생성 함수
function generateCalendar(year, month = null) {
  if (calendar) {
    calendar = null;
    // 이전 달력 삭제
    while (calendarArea.childElementCount > 1) {
      calendarArea.children[1].remove();
    }
    noteArea.innerHTML = "";
  }
  console.log(`Calendar is running! ${year} ${month + 1}`);

  // 이전 달/연도 버튼
  const prevButton = document.createElement("a");
  prevButton.href = "#";
  prevButton.innerHTML = "<";
  prevButton.className = "btn-prev";
  prevButton.addEventListener("click", function () {
    if (month === null) {
      const prevYear = new Date(year, month);
      calendar = generateCalendar( prevYear.getFullYear() - 1);
      fetchAndDisplaySchedules();
      if (calendar.month == currentDate.getMonth()) {
        calendar.Dates[currentDate.getDate() - 1].showNoteForDate();
      } else {
        calendar.Dates[calendar.monthStart.getDate() - 1].showNoteForDate();
      }

    } else {
      const prevMonth = new Date(year, month - 1);
      calendar = generateCalendar( prevMonth.getFullYear(), prevMonth.getMonth());
      fetchAndDisplaySchedules();
      if (calendar.month == currentDate.getMonth()) {
        calendar.Dates[currentDate.getDate() - 1].showNoteForDate();
      } else {
        calendar.Dates[calendar.monthStart.getDate() - 1].showNoteForDate();
      }
    }
  });

  // 다음 달/연도 버튼
  const nextButton = document.createElement("a");
  nextButton.href = "#";
  nextButton.innerHTML = ">";
  nextButton.className = "btn-next";
  nextButton.addEventListener("click", function () {
    if (month === null) {
      const nextYear = new Date(year, month);
      calendar = generateCalendar( nextYear.getFullYear() + 1);
      fetchAndDisplaySchedules();
      if (calendar.month == currentDate.getMonth()) {
        calendar.Dates[currentDate.getDate() - 1].showNoteForDate();
      } else {
        calendar.Dates[calendar.monthStart.getDate() - 1].showNoteForDate();
      }
    } else {
      const nextMonth = new Date(year, month + 1);
      calendar = generateCalendar( nextMonth.getFullYear(), nextMonth.getMonth());
      fetchAndDisplaySchedules();
      if (calendar.month == currentDate.getMonth()) {
        calendar.Dates[currentDate.getDate() - 1].showNoteForDate();
      } else {
        calendar.Dates[calendar.monthStart.getDate() - 1].showNoteForDate();
      }
    }
  });

  // 연도와 월 표시
  const headerTitle = document.createElement("div");
  headerTitle.innerHTML = month === null ? year + "년 " : year + "년 " + (month + 1) + "월";
  headerTitle.className = "calendar-title";
  headerTitle.addEventListener("click", function () {
    generateCalendar( year);
  });

  // 이전 달력 삭제
  while (calendarArea.childElementCount > 1) {
    calendarArea.children[1].remove();
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
    generateYearCalendar(year);
  } else {
    // 월 달력
    return generateMonthCalendar(year, month);
  }
}
// 연도별 달력
function generateYearCalendar(year) {
  const monthContainer = document.createElement("div");
  monthContainer.className = "calendar-months";
  for (let i = 0; i < 12; i++) {
    const monthCell = document.createElement("div");
    monthCell.innerHTML = i + 1 + "월";
    monthCell.className = "calendar-month";
    monthCell.addEventListener("click", function () {
      generateCalendar( year, i);
    });
    monthContainer.appendChild(monthCell);
  }
  calendarArea.appendChild(monthContainer);
}
// 월별 달력
function generateMonthCalendar(year, month) {
  const calendar = new MonthCalendar(year, month);

  // 요일 헤더 생성
  const daysRow = document.createElement("div");
  daysRow.className = "day-row"; // grid-row repeat(7, 1fr)
  calendar.days.forEach(day => {
    const dayCell = document.createElement("div");
    dayCell.innerHTML = `<div class="square"><div class="inner"><div class="calendar-day">${day}</div></div></div>`;
    daysRow.appendChild(dayCell);
  });

  // 날짜 채우기
  const dateContainer = document.createElement("div");
  dateContainer.className = "date-container"; // grid-row repeat(7, 1fr)

  calendar.beforeMonthDates.forEach(date => {
    date.drawDateCell(dateContainer, 'calendar-date other-month' );
  });
  calendar.Dates.forEach(date => {
    date.drawDateCell(dateContainer, 'calendar-date' );
  });
  calendar.afterMonthDates.forEach(date => {
    date.drawDateCell(dateContainer, 'calendar-date other-month');
  });

  calendarArea.appendChild(daysRow);
  calendarArea.appendChild(dateContainer);

  return calendar;
}
// 스케쥴 가져오기 함수
function fetchAndDisplaySchedules() {
  try {
    // schedule 요청
    // const response = await axios({
    axios({
      method: 'get',
      url: `schedules/?year=${calendar.year}&month=${calendar.month + 1}`,
      responseType: 'json',
    }).then(response => {
      // 스케쥴 초기화
      calendar.schedules = new Array();
      response.data.forEach(item => {
        const schedule = new Schedule(
          item.id,
          item.calendar,
          item.start,
          item.end,
          item.summary,
          item.location,
          item.description
        );
        calendar.schedules.push(schedule);
      });
      return calendar
    }).then(calendar => {
      // 스케쥴 바 표시
      calendar.schedules.forEach(schedule => {
        schedule.createScheduleBars(calendar);
      })
      calendar.Dates[currentDate.getDate() - 1].showNoteForDate();
    });
  } catch (error) {
    console.error(error);
  };
}
function createSchedule(form) {
  try {
    axios({
      method: 'post',
      url: `schedules/`,
      data: {
        'start': form.querySelector('input[name="start"]').value,
        'end': form.querySelector('input[name="end"]').value,
        'location': form.querySelector('input[name="location"]').value,
        'summary': form.querySelector('input[name="summary"]').value,
        'description': form.querySelector('input[name="description"]').value,
        'calendar': form.querySelector('select[name="calendar"]').value,
      },
    }).then(response => {
      calendar.cleanCalendar();
    }).then(function () {
      fetchAndDisplaySchedules();
      const scheduleDate = new Date(form.querySelector('input[name="start"]').value)
      calendar.Dates[scheduleDate.getDate() - 1].showNoteForDate();
    });
  } catch (error) {
    console.error(error);
  }
}
function deleteSchedule(form) {
  try {
    axios({
      method: 'delete',
      url: `schedules/${form.dataset.scheduleId}/`,
    }).then(response => {
      calendar.cleanCalendar();
    }).then(function () {
      fetchAndDisplaySchedules();
      calendar.Dates[currentDate.getDate() - 1].showNoteForDate();
    });
  } catch (error) {
    console.error(error);
  }
}
function updateSchedule(form) {
  try {
    axios({
      method: 'put',
      url: `schedules/${form.dataset.scheduleId}/`,
      data: {
        'start': form.querySelector('input[name="start"]').value,
        'end': form.querySelector('input[name="end"]').value,
        'location': form.querySelector('input[name="location"]').value,
        'summary': form.querySelector('input[name="summary"]').value,
        'description': form.querySelector('input[name="description"]').value,
        'calendar': form.dataset.calendarId
      },
    }).then(response => {
      calendar.cleanCalendar();
    }).then(function () {
      fetchAndDisplaySchedules();
      const scheduleDate = new Date(form.querySelector('input[name="start"]').value)
      calendar.Dates[scheduleDate.getDate() - 1].showNoteForDate();
    });
  } catch (error) {
    console.error(error);
  }
}
function fetchGroupsAndCreateFilters() {
  try {
    axios({
      method: 'get',
      url: `../../../../groups/search?q= `,
      responseType: 'json',
    })
      .then(function (response) {
        // console.log('fetch user_groups')
        GroupDict = {};
        CalendarDict = {};
        var colorIndex = 0
        GroupDict['user']={'name':'user', 'calendar':userCalendarId, 'color':0, 'thumbnail':'#'}
        CalendarDict[userCalendarId]={'name':'user', 'group':'user', 'color':0}
        const groupButton = document.createElement("button")
        groupButton.classList = "filter-button"
        const square = document.createElement("div");
        square.className = "square";
        const inner = document.createElement("div");
        inner.className = "inner";
        inner.setAttribute("style", `background-color:var(--color-id-${colorIndex});`);
        square.appendChild(inner)
        groupButton.appendChild(square)
        filterArea.appendChild(groupButton)
        response.data.forEach(item => {
          colorIndex += 1;
          GroupDict[item.id] = {'name':item.name, 'calendar':item.calendar, 'color': colorIndex, 'thumbnail': item.thumbnail};
          CalendarDict[item.calendar] = {'name':item.name, 'group':item.id, 'color': colorIndex};

          const groupButtonClone = groupButton.cloneNode(true)
          groupButtonClone.firstChild.firstChild.setAttribute("style", `background-color:var(--color-id-${colorIndex});`);
          filterArea.appendChild(groupButtonClone)
          colorIndex = colorIndex%8;
        })
      }).then(function() {
        fetchAndDisplaySchedules();
        calendar.Dates[currentDate.getDate() - 1].showNoteForDate();
      });
  } catch (error) {
    console.error(error)
  }
}
//import axios from 'axios';
const csrftoken = Cookies.get('csrftoken');
axios.defaults.headers.common['X-CSRFToken'] = csrftoken;
// Group과 Calendar
var GroupDict = {};
var CalendarDict = {};
// 현재 날짜로 달력 생성
const currentDate = new Date();
const calendarArea = document.getElementById('calendar-area');
const noteArea = document.getElementById('note-area');
const filterArea = document.getElementById('filter-area');
const days = ["일", "월", "화", "수", "목", "금", "토"];
const userCalendarId = document.getElementById('dataset').dataset.userCalendarId;

// 스케쥴 가져오기
var calendar = generateCalendar(currentDate.getFullYear(), currentDate.getMonth());
fetchGroupsAndCreateFilters();
// 현재 날짜의 노트 표시
const COLORS = ['#9DC8C8', '#D1B6E1', '#82C0E4', '#FEEE7D', '#F7AA97', '#F1BBBA', '#88DBA3'];