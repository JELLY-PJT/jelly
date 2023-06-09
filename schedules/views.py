from schedules.models import *
from schedules.serializers import *
"""
for authentication and permissions
"""
from rest_framework import permissions
"""
for query & logic
"""
from django.db.models import Q
from rest_framework import viewsets
"""
for response
"""
from django.shortcuts import render, redirect
from rest_framework.response import Response


# Create your views here.
"""
lookups keyword : field__lookuptype=value
"""

# '~/schedules/calendars'
class UserCalendarViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CalendarSerializer
    def get_queryset(self):
        """
        현재 로그인한 user의 모든 calendar를 list
        """
        user = self.request.user
        queryset = Calendar.objects.filter(Q(owner_group__in=user.user_groups.all()) | Q(owner_user__exact=user))
        return queryset

#'~/schedules/calendars/<int:calendar_id>/schedules'
class CalendarScheduleViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ScheduleSerializer
    def get_queryset(self):
        """
        해당 calendar의 모든 schedule을 list
        """
        q = self.kwargs
        user = self.request.user
        calendar = Calendar.objects.get(id=q['calendar_id'])
        user_calendar_set = Calendar.objects.filter(Q(owner_group__in=user.user_groups.all()) | Q(owner_user__exact=user))
        if calendar in user_calendar_set:
            queryset = calendar.schedules.all()
        else:
            queryset = None
        return queryset

    def perform_create(self, serializer):
        serializer.save(calendar_id=self.kwargs['calendar_id'])


# superuser only
class ScheduleViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer    

# superuser only
class CalendarViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer
