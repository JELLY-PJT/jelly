from django.db import models
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field
from datetime import datetime, timedelta
from django.utils import timezone
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from urllib.parse import urljoin


# Create your models here.
class Diary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = CKEditor5Field('Content', config_name='extends')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    share = models.ManyToManyField('groups.Group', related_name='group_diaries', verbose_name='shared diary to group', through='DiaryShare')
    hit = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='diary_views')
    thumbnail =  models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.title
    
    def get_model_name(self):
        return self._meta.model_name

    def increase_hit(self, user):
        diary_share, created = DiaryShare.objects.get_or_create(diary=self)

        if user not in diary_share.hit.all():
            diary_share.hit.add(user)

    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.created_at
        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(time.seconds // 60) + '분 전'
        elif time < timedelta(days=1):
            return str(time.seconds // 3600) + '시간 전'
        elif time < timedelta(weeks=1):
            time = datetime.now(tz=timezone.utc).date() - self.created_at.date()
            return str(time.days) + '일 전'
        else:
            return self.created_at.strftime('%Y-%m-%d')


class DiaryShare(models.Model):
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    group = models.ForeignKey('groups.Group', on_delete=models.CASCADE)
    shared_at = models.DateTimeField(auto_now_add=True)

    @property
    def shared_string(self):
        time = datetime.now(tz=timezone.utc) - self.shared_at
        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(time.seconds // 60) + '분 전'
        elif time < timedelta(days=1):
            return str(time.seconds // 3600) + '시간 전'
        elif time < timedelta(weeks=1):
            time = datetime.now(tz=timezone.utc).date() - self.shared_at.date()
            return str(time.days) + '일 전'
        else:
            return self.shared_at.strftime('%Y-%m-%d')


class DiaryComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    share = models.ForeignKey(DiaryShare, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_diarycomments')
    
    class Meta:
         ordering = ['-created_at']


class DiaryEmote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='emotions')
    share = models.ForeignKey(DiaryShare, on_delete=models.CASCADE)
    emotion = models.PositiveIntegerField()
    class Meta:
        unique_together = [['user', 'share']]
    # 1:👍 2:🥰 3:🤣 4:😲 5:😭 6:🥳