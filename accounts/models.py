from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from django.contrib.contenttypes import fields

# Create your models here.
class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        user = super()._create_user(username, email, password, **extra_fields)
        user.calendar.create()
        return user


class User(AbstractUser):
    nickname = models.CharField(max_length=20)
    #프로필 이미지 원본을 저장할지 논의
    image = ProcessedImageField(upload_to='users', 
                                blank=True,
                                processors=[Thumbnail(100,100)],
                                format='JPEG',
                                options={'quality': 80})
    """
    for calendar model
    """
    calendar = fields.GenericRelation('schedules.Calendar', object_id_field='owner_object_id', content_type_field='owner_content_type', related_query_name='owner_user')
    objects = UserManager()



