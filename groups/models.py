from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.contenttypes import fields


class GroupManager(models.Manager):
    def create(self, **kwargs):
        group = super().create(**kwargs)
        group._calendar.create()
        return group


class Group(models.Model):
    chief = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_groups')
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    _calendar = fields.GenericRelation('schedules.Calendar', object_id_field='owner_object_id', content_type_field='owner_content_type', related_query_name='owner_group')

    def group_image_path(instance, filename):
        return f'groups/{instance.name}_{instance.pk}/{filename}'
    
    thumbnail = ProcessedImageField(upload_to=group_image_path, blank=True,
                                    processors=[ResizeToFill(500,500)],
                                    format='JPEG',
                                    options={'quality': 100})
    intro = models.CharField(max_length=500)
    exp = models.PositiveIntegerField()
    level = models.PositiveIntegerField()
    # 기준 = 경험치/(그룹인원**0.5)
    # lv.1 : 새싹 단계, 기준 < 10       
    # lv.2 : 풀 단계, 기준 < 30          lv.7 : 판다 단계, 기준 < 280
    # lv.3 : 나무 단계, 기준 < 60        lv.8 : 레서판다 단계, 기준 < 360
    # lv.4 : 개화 단계, 기준 < 100       lv.9 : 유니콘 단계, 기준 < 450
    # lv.5 : 열매 단계, 기준 < 150       lv.10 : 뿔 달린 유니콘 단계, 기준 < 550
    # lv.6 : 반달곰 단계, 기준 < 210     lv.11 : 날개 달린 유니콘 단계, 기준 < 660

    created_at = models.DateTimeField(auto_now_add=True)

    objects = GroupManager()

    def __str__(self):
        return self.name
    
    @property
    def calendar(self):
         return self._calendar.all()[0]


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    # schedule = models.ForeignKey('schedules.GroupSchedule', on_delete=models.CASCADE, blank=True)
    hits = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='post_views')
    emote_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='emote_posts', through='PostEmote')
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_notice = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_model_name(self):
        return self._meta.model_name

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
    

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def post_image_path(instance, filename):
        now = instance.post.created_at
        return f'groups/{instance.post.group.name}_{instance.post.group.pk}/' + now.strftime('%Y/%m/%d') + f'/{filename}'
    
    image = ProcessedImageField(upload_to=post_image_path, blank=True,
                                processors=[ResizeToFill(500,500)],
                                format='JPEG',
                                options={'quality': 100})


class PostEmote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    emotion = models.PositiveIntegerField()
    # 1:👍 2:🥰 3:🤣 4:😲 5:😭 6:🥳


class PostComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_post_comments')
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    hits = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='vote_views')
    title = models.CharField(max_length=100)
    deadline = models.DateTimeField()
    is_notice = models.BooleanField()
    is_overlap = models.BooleanField()
    is_annony = models.BooleanField()
    is_addible = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_model_name(self):
        return self._meta.model_name

    def d_day(self):
        time = self.deadline - datetime.now(tz=timezone.utc)
        if time < timedelta(seconds=1):
            return '투표 마감'
        elif time < timedelta(minutes=1):
            return '곧 마감'
        elif time < timedelta(hours=1):
            return str(time.seconds // 60) + '분 후 마감'
        elif time < timedelta(days=1):
            return str(time.seconds // 3600) + '시간 후 마감'
        else:
            return 'D-' + str(time.days)
    
    def is_end(self):
        if datetime.now(tz=timezone.utc) > self.deadline:
            return True
        else:
            return False

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


class VoteSelect(models.Model):
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    select_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='selections')
    content = models.CharField(max_length=100)


