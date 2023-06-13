import { generateCalendar } from '../../js/schedules/Calendar.js';
import { Schedule } from '../../js/schedules/Schedule.js';


// 스케쥴 가져오기 함수
async function fetchAndDisplaySchedules(calendar) {
  try {
    // schedule 요청
    // const response = await axios({
    axios({
      method: 'get',
      url: `calendars/schedules/?year=${calendar.year}&month=${calendar.month + 1}`,
      responseType: 'json',
    }) .then (response => {
      // 캘린더에 추가
      calendar.schedules = [];
      response.data.forEach(item => {
        const schedule = new Schedule(
          item.id,
          item.calendar,
          item.start,
          item.end,
          item.summary,
          item.location,
          item.attendee,
          item.description
        );

        calendar.schedules.push(schedule);
      });


      // 현재 날짜의 노트 표시
      calendar.Dates[currentDate.getDate()-1].showNoteForDate(noteArea);

      calendar.gridStatus = [];
      var r = [0, 0, 0]
      for (var i = 0; i < calendar.monthEndDate; i++) {
        calendar.gridStatus.push([...r]);
      }

      calendar.schedules.forEach(schedule => {
        schedule.createScheduleBars(calendar);
      })
    })
    

    

  } catch (error) {
    console.error(error);
  };
}

// 현재 날짜로 달력 생성
const currentDate = new Date();
const calendarArea = document.getElementById('calendar-area');
const noteArea = document.getElementById('note-area');

// 스케쥴 가져오기
const calendar = generateCalendar(calendarArea, noteArea, currentDate.getFullYear(), currentDate.getMonth());
fetchAndDisplaySchedules(calendar);