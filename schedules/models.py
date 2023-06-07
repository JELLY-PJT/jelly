from django.db import models
from django.utils import timezone
# Create your models here.
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.contrib.contenttypes import fields
from django.contrib.auth import get_user_model
from django.conf import settings
from groups.models import Group
from django.contrib.contenttypes import fields
from django.contrib.auth.models import UserManager


# 캘린더
class Calendar(models.Model):
    owner_content_type = models.ForeignKey(ContentType, limit_choices_to=Q(app_label='accounts', model='user') | Q(app_label='groups', model='group'), on_delete=models.DO_NOTHING)
    owner_object_id = models.PositiveIntegerField()
    owner = fields.GenericForeignKey('owner_content_type', 'owner_object_id')
    color = models.CharField(
        max_length=6, 
        default="000000"
    )

    def __str__(self):
        return f'{self.id} {self.get_title()}'
    
    class Meta:
        indexes = [models.Index(fields=["owner_content_type", "owner_object_id"]),]

    def get_owner(self):
        if self.owner_content_type_id == 1:
            try:
                owner = get_user_model().objects.get(pk=self.owner_object_id)
                return owner
            except:
                return None
             
        elif self.owner_content_type_id == 2:
            try:
                owner = Group.objects.get(pk=self.owner_object_id)
                return owner
            except:
                return None
        else:
            return None
        
    def get_title(self):
        if self.owner_content_type_id == 1:
            try:
                owner = get_user_model().objects.get(pk=self.owner_object_id)
                return f'{owner.username}의 개인 캘린더'
            except:
                return None
             
        elif self.owner_content_type_id == 2:
            try:
                owner = Group.objects.get(pk=self.owner_object_id)
                return f'{owner.name}의 그룹 캘린더'
            except:
                return None
        else:
            return None


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
    

class CustomUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        user = super()._create_user(self, username, email, password, **extra_fields)
        user.calendar.create()
        return user
    
class CustomGroupManager(UserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        user = super()._create_user(self, username, email, password, **extra_fields)
        user.calendar.create()
        return user
    