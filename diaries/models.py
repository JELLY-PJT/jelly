from django.db import models
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.
class Diary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = CKEditor5Field('Content', config_name='extends')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    share = models.ManyToManyField('groups.Group', verbose_name='shared diary to group', through='DiaryShare')
    # hit = models.ManyToManyField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.title
    
    def increase_hit(self, user):
        diary_share, created = DiaryShare.objects.get_or_create(diary=self)

        if user not in diary_share.hit.all():
            diary_share.hit.add(user)


class DiaryShare(models.Model):
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    group = models.ForeignKey('groups.Group', on_delete=models.CASCADE)
    shared_at = models.DateTimeField(auto_now_add=True)
    

class DiaryComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    group = models.ForeignKey('groups.Group', on_delete=models.CASCADE)
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_diarycomments')

    class Meta:
        ordering = ['-created_at']


class DiaryEmote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='emotions')
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    emotion = models.PositiveIntegerField()
    # 1:👍 2:🥰 3:🤣 4:😲 5:😭 6:🥳

    # class Meta:
    #     ordering = ['-created_at']

