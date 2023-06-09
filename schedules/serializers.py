from rest_framework import serializers
from groups.models import Group
from django.contrib.auth import get_user_model
from .models import Calendar, Schedule
from django.utils.translation import gettext_lazy as _




class CalendarSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    schedules = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='preview'
    )
    color = serializers.CharField()

    class Meta:
        model = Calendar
        fields =  ['id', 'owner', 'color', 'schedules']

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'
        read_only_fields = ['attendee', 'calendar']