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
import datetime
"""
for response
"""
from django.shortcuts import render, redirect
from rest_framework.response import Response


# Create your views here.
"""
lookups keyword : field__lookuptype=value
"""

#'groups/<int:group_pk>/calendars/schedules'
class GroupScheduleViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        """
        해당 group의 schedule을 list
        """
        user, calendar_id = self.request.user, Calendar.objects.get(owner_group__pk=self.kwargs['group_pk']).pk
        year = int(self.request.GET.get('year', timezone.now().year))
        month = int(self.request.GET.get("month", timezone.now().month))
        if calendar_id in user.permitted_calendar_id:
            self.queryset = Calendar.objects.get(pk=calendar_id).schedules.filter(Q(start__year__lte=year) & Q(start__month__lte=month)).filter(Q(end__year__gte=year) & Q(end__month__gte=month))
        else:
            self.queryset = Schedule.objects.none() # empty queryset
        return super().get_queryset()

    def perform_create(self, serializer):
        calendar_id = Calendar.objects.get(owner_group__pk=self.kwargs['group_pk']).pk
        serializer.save(calendar_id=calendar_id)

    def perform_update(self, serializer):
        calendar_id = Calendar.objects.get(owner_group__pk=self.kwargs['group_pk']).pk
        serializer.save(calendar_id=calendar_id)

#'accounts/profile//<username>/calendar/schedules'
class UserScheduleViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ScheduleSerializer
    def get_queryset(self):
        """
        해당 user 와 user_groups의 모든 schedule을 list
        """
        user = self.request.user
        year = int(self.request.GET.get('year', timezone.now().year))
        month = int(self.request.GET.get("month", timezone.now().month))

        calendars = Calendar.objects.filter(pk__in=user.permitted_calendar_id)
        queryset = Calendar.objects.filter(pk__in=user.permitted_calendar_id).select_related('schedules').values_list('schedules', flat=False)
        self.queryset = Schedule.objects.filter(id__in=queryset).filter(Q(start__year__lte=year) & Q(start__month__lte=month)).filter(Q(end__year__gte=year) & Q(end__month__gte=month))
        return super().get_queryset()

    def perform_create(self, serializer):
        print(self.request)
        print("**********************")
        print(self.request.data)
        print("**********************")
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

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
