from rest_framework import serializers
from .models import Calendar, Schedule
from django.utils.translation import gettext_lazy as _




class CalendarSerializer(serializers.ModelSerializer):
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
    # description = serializers.CharField(
    #     style={'base_template': 'textarea.html'}
    # )
    class Meta:
        model = Schedule
        fields = ['calendar', 'start', 'end', 'summary', 'location', 'attendee', 'description']
        read_only_fields = ['attendee', 'calendar']