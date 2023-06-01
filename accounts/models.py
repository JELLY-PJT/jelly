from django.db import models

from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
# Create your models here.

class User(AbstractUser):
    nickname = models.CharField(max_length=20)
    #프로필 이미지 원본을 저장할지 논의
    image = ProcessedImageField(upload_to='users', 
                                blank=True,
                                processors=[Thumbnail(100,100)],
                                format='JPEG',
                                options={'quality': 80})