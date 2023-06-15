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
        scheduleBar['body'].setAttribute(
          "style", 
          `width:calc(var(--date-cell-width) * ${scheduleBar['width']} - 1px);
          max-width:calc(var(--date-cell-max-width) * ${scheduleBar['width']} - 1px);`);
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
    const form = document.createElement("form");
    form.classList = "schedule-form";
    form.setAttribute('id', `schedule-form-${this.id}`);
    form.setAttribute('action',"#" );
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
    formInputArea.innerHTML=`
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