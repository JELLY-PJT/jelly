export class Schedule {
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
    this.startDate_Date = new Date(this.startDate.toDateString())
    this.endDate = new Date(this.end);
    this.endDate_Date = new Date(this.endDate.toDateString())
  }

  createScheduleBars(calendar) {
    console.log("create schedule bar");
    // create ScheduleBars
    this.scheduleBars = [];
    this.scheduleBarWidth = 1 + Math.floor((Math.min(calendar.calendarEndDate, this.endDate_Date)-this.startDate_Date)/(1000*60*60*24)); 
    console.log(this.scheduleBarWidth);
    if (this.startDate.getMonth() == calendar.month) {

      for( var i=this.startDate.getDate(); i < Math.min(this.startDate.getDate() + this.scheduleBarWidth, calendar.monthEndDate); i++){
        if (!calendar.Dates[i - 1].schedules) {
          calendar.Dates[i - 1].schedules = [];
        }
        calendar.Dates[i - 1].schedules.push(this);
      }
    }


    
    const scheduleBarBody = document.createElement("div");
    for (var i = 0; i < this.scheduleBarWidth; i += 7) {
      if (i == 0) {
        const scheduleBar = { body: scheduleBarBody.cloneNode(true), width: Math.min(this.scheduleBarWidth, 7 - this.startDate.getDay()), }
        scheduleBar['body'].className = "schedule-bar";
        scheduleBar['body'].innerHTML = `<p>${this.summary}</p>`;
        scheduleBar['body'].setAttribute("style", `width:calc(var(--date-cell-width) * ${scheduleBar['width']} - 1px);`);
        i += scheduleBar['width']
        this.scheduleBars.push(scheduleBar);
      } else if (i + 7 < this.scheduleBarWidth) {
        const scheduleBar = { body: scheduleBarBody.cloneNode(true), width: 7, }
        scheduleBar['body'].className = "schedule-bar";
        scheduleBar['body'].innerHTML = `<p>${this.summary}</p>`;
        scheduleBar['body'].setAttribute("style", `width:calc(var(--date-cell-width) * ${scheduleBar['width']} - 1px);`);
        i += scheduleBar['width']
        this.scheduleBars.push(scheduleBar);

      } else {
        const scheduleBar = { body: scheduleBarBody.cloneNode(true), width: (this.scheduleBarWidth - Math.min(this.scheduleBarWidth, 7 - this.startDate.getDay()))%7}
        scheduleBar['body'].className = "schedule-bar";
        scheduleBar['body'].innerHTML = `<p>${this.summary}</p>`;
        scheduleBar['body'].setAttribute("style", `width:calc(var(--date-cell-width) * ${scheduleBar['width']} - 1px);`);
        i += scheduleBar['width']
        this.scheduleBars.push(scheduleBar);
      }
    }
    this.displayScheduleBars(calendar);
  }

  displayScheduleBars(calendar) {
    console.log("displayScheduleBars");
    var r = calendar.checkGridStatus(this);
    if (r) {
      var i = this.startDate.getDate();
      this.scheduleBars.forEach(scheduleBar => {
        calendar.getGridCell(i, r).appendChild(scheduleBar['body']);
        i += scheduleBar['width'];
      });
    }
  }

    // TODO :  make scheduleBar dragable, add drag EventListner, add doubleclick EnvetListner -> modal..

  note() {
    const ScheduleNote = document.createElement("div");
    ScheduleNote.classList = "schedule-note";
    ScheduleNote.innerHTML = `
      <p> ✅ ${this.summary}</p>
      <p>시작 : ${this.startDate.toLocaleString('ko-KR', { dateStyle: 'medium', timeStyle: 'short', timeZone: 'UTC' })}</p>
      <p>종료 : ${this.endDate.toLocaleString('ko-KR', { dateStyle: 'medium', timeStyle: 'short', timeZone: 'UTC' })}</p>
      <p>장소 : ${this.location}</p>
      <p>참석자 : ${this.attendee}</p>
      <p>상세 : ${this.description}</p>`;
    return ScheduleNote
  }
}
