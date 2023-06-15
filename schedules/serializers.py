from rest_framework import serializers
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
        fields =  ['id', 'owner', 'color', 'schedules']

class ScheduleSerializer(serializers.ModelSerializer):
    # description = serializers.CharField(
    #     style={'base_template': 'textarea.html'}
    # )
    # start_date = serializers.DateField(source='start__date', read_only=True, required=False)
    # start_time = serializers.TimeField(source='start__time', read_only=True, required=False)
    # end_date = serializers.DateField(source='end__date', read_only=True, required=False)
    # end_time = serializers.TimeField(source='end__time', read_only=True, required=False)
    # start_time = serializers.TimeField(
    #     time_field = 'start__time'
    # )
    # end_date = serializers.DateField(
    #     date_field = 'end__date'
    # )
    # end_time = serializers.TimeField(
    #     time_field = 'end__time'
    # )
# 'start', 'end', 'summary', 'location', 'description'
    # attendee = serializers.SlugRelatedField(
    #     many=True,
    #     slug_field="name",
    #     read_only=True,
    # )
    class Meta:
        model = Schedule
        # fields = ['id', 'calendar', 'start', 'end', 'summary', 'location', 'attendee', 'description']
        fields = ['id', 'calendar', 'start', 'end', 'summary', 'location', 'description']
        read_only_fields = ['calendar']
