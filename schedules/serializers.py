from rest_framework import serializers
from groups.models import Group
from django.contrib.auth import get_user_model
from .models import Calendar, Schedule
from django.utils.translation import gettext_lazy as _

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class CalendarSerializer(serializers.ModelSerializer):
    schedules = serializers.SlugRelatedField(
        many=True,
        slug_field='summary',
        read_only=True,
    )
    class Meta:
        model = Calendar
        fields =  '__all__'