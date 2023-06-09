from django.db import models
from django.contrib.auth.models import UserManager
from django.utils import timezone
# Create your models here.
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.contrib.contenttypes import fields
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.contenttypes import fields


# 캘린더
class Calendar(models.Model):
    owner_content_type = models.ForeignKey(ContentType, editable=False, limit_choices_to=Q(app_label='accounts', model='user') | Q(app_label='groups', model='group'), on_delete=models.DO_NOTHING)
    owner_object_id = models.PositiveIntegerField(editable=False)
    owner = fields.GenericForeignKey('owner_content_type', 'owner_object_id')
    color = models.CharField(
        max_length=6, 
        default="000000"
    )

    def __str__(self):
        return f'{self.owner_content_type.name} "{self.owner}"의  캘린더'
    @property
    def belongs_to(self):
        return f'{self.owner}'
    
    class Meta:
        indexes = [models.Index(fields=["owner_content_type", "owner_object_id"]),]

# 스케쥴
class Schedule(models.Model):
    start = models.DateTimeField(default=timezone.now) # 시작 일시
    end = models.DateTimeField(blank=True, null=True) # 종료 일시

    summary = models.CharField(max_length=150, blank=True, default="") # 일정 제목
    description = models.CharField(max_length=255, blank=True, default="") # 일정 상세 내용
    location = models.CharField(max_length=255, blank=True, default="") # 장소

    calendar = models.ForeignKey('schedules.Calendar', on_delete=models.CASCADE, related_name='schedules') # 일정 소속 캘린더
    attendee = models.ManyToManyField(settings.AUTH_USER_MODEL)

    created_at = models.DateTimeField(auto_now_add=True) # 일정 생성시각
    updated_at = models.DateTimeField(auto_now=True) # 일정 수정시각


    # # Month and day names.  For localized versions, see the calendar module.
    # _DAYNAMES = [None, "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    def __str__(self):
        _MONTHNAMES = [None, "Jan", "Feb", "Mar", "Apr", "May", "Jun",
                         "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        startdate = f'{_MONTHNAMES[self.start.month]} {self.start.day}'
        time = [f'{self.start.time}' , f'{self.end.time}']

        return f'({startdate}) {self.summary[:32]}'
    
    @property
    def preview(self):
        return f'{self.start} ~ {self.end} : {self.summary[:32]}'
    
"""
scheduleIcalString += "DTSTART;TZID=Asia/Seoul:20161116T190000\n"     # 시작 일시
scheduleIcalString += "DTEND;TZID=Asia/Seoul:20161116T193000\n"       # 종료 일시
"""