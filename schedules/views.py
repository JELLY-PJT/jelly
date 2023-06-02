from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import ScheduleForm, GroupScheduleForm
from .models import Schedule, GroupSchedule

# Create your views here.
def create(request):

    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.user = request.user
            schedule.save()
            return redirect('groups:index')
    else:
        form = ScheduleForm()
    context = {
        'form': form,
    }
    return render(request, 'schedules/create.html', context)


def today(request):
    current_date = timezone.now()

    schedules = Schedule.objects.filter(
        user=request.user,  # 사용자
        startdate__lte=current_date,  # 시작일이 오늘 이하
        finishdate__gte=current_date  # 종료일이 오늘 이상
    )

    context = {
        'schedules': schedules,
    }
    return render(request, 'schedules/', context) # 탬플릿 입력 필요


def thisweek(request):
    current_date = timezone.now()
    
    start_of_week = current_date - timezone.timedelta(days=current_date.weekday())
    end_of_week = start_of_week + timezone.timedelta(days=6)

    schedules = Schedule.objects.filter(
        user=request.user,  # 사용자
        startdate__lte=end_of_week  # 시작일이 이번 주인 스케줄
    ) | Schedule.objects.filter(
        user=request.user,  # 사용자
        finishdate__gte=start_of_week  # 종료일이 이번 주인 스케줄
    )

    context = {
        'schedules': schedules,
    }
    return render(request, 'schedules/', context) # 탬플릿 입력 필요


def thismonth(request):
    current_date = timezone.now()

    start_of_month = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    next_month = start_of_month.replace(month=start_of_month.month+1)
    end_of_month = next_month - timezone.timedelta(days=1)

    schedules = Schedule.objects.filter(
        user=request.user,  # 사용자
        startdate__lte=end_of_month  # 시작일이 이번 달인 스케줄
    ) | Schedule.objects.filter(
        user=request.user,  # 사용자
        finishdate__gte=start_of_month  # 종료일이 이번 달인 스케줄
    )

    context = {
        'schedules': schedules,
    }
    return render(request, 'schedules/', context) # 탬플릿 입력 필요


def themonth(request, year, month):

    start_of_month = timezone.datetime(year=year, month=month, day=1)
    next_month = start_of_month.replace(month=start_of_month.month+1)
    end_of_month = next_month - timezone.timedelta(days=1)

    schedules = Schedule.objects.filter(
        user=request.user,  # 사용자
        startdate__lte=end_of_month  # 시작일이 특정 달인 스케줄
    ) | Schedule.objects.filter(
        user=request.user,  # 사용자
        finishdate__gte=start_of_month  # 종료일이 특정 달인 스케줄
    )

    context = {
        'schedules': schedules,
    }
    return render(request, 'schedules/', context) # 탬플릿 입력 필요


def theday(request, year, month, day):

    theday = timezone.datetime(year=year, month=month, day=day)

    schedules = Schedule.objects.filter(
        user=request.user,  # 사용자
        startdate__lte=theday,  # 시작일이 특정일 이하
        finishdate__gte=theday  # 종료일이 특정일 이상
    )

    context = {
        'schedules': schedules,
    }
    return render(request, 'schedules/', context) # 탬플릿 입력 필요