from django.db import models
from django.conf import settings

# Create your models here.
class Schedule(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    note = models.TextField()
    startdate = models.DateTimeField(auto_now=False, auto_now_add=False)
    finishdate = models.DateTimeField(auto_now=False, auto_now_add=False)


class GroupSchedule(models.Model):
    group = models.ForeignKey('groups.Group', on_delete=models.CASCADE)
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    note = models.TextField()
    startdate = models.DateTimeField(auto_now=False, auto_now_add=False)
    finishdate = models.DateTimeField(auto_now=False, auto_now_add=False)
    join_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='join_schedules')