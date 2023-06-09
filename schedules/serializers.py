from rest_framework import serializers
from groups.models import Group
from django.contrib.auth import get_user_model
from .models import Calendar, Schedule
from django.utils.translation import gettext_lazy as _




class CalendarSerializer(serializers.ModelSerializer):
    schedules = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='preview'
    )
    class Meta:
        model = Calendar
        fields =  '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'
        read_only_fields = ['attendee', 'calendar']