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

# '~/schedules/calendars'
# class UserCalendarViewSet(viewsets.ReadOnlyModelViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = CalendarSerializer
#     def get_queryset(self):
#         """
#         현재 로그인한 user의 모든 calendar를 list
#         """
#         user = self.request.user
#         self.queryset = Calendar.objects.filter(id__in=user.permitted_calendar_id)
#         return super().get_queryset()

#'groups/<int:group_pk/calendars/schedules'
class GroupScheduleViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ScheduleSerializer
    def get_queryset(self):
        """
        해당 group의 schedule을 list
        """
        user, calendar_id = self.request.user, Calendar.objects.get(owner_group__pk=self.kwargs['group_pk']).pk
        print(self.request.GET)
        year, month = int(self.request.GET["year"]), int(self.request.GET["month"])
        if calendar_id in user.permitted_calendar_id:
            self.queryset = Calendar.objects.get(pk=calendar_id).schedules.filter(Q(start__year__lte=year) & Q(start__month__lte=month)).filter(Q(end__year__gte=year) & Q(end__month__gte=month))
            print(self.queryset)
        else:
            self.queryset = Schedule.objects.none() # empty queryset
        return super().get_queryset()

    def perform_create(self, serializer):
        calendar_id = self.request.user, Calendar.objects.get(owner_group__pk=self.kwargs['group_pk']).pk
        serializer.save(calendar_id=calendar_id)

#'accounts/calendars/schedules'
class UserScheduleViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ScheduleSerializer
    def get_queryset(self):
        """
        해당 user 와 user_groups의 모든 schedule을 list
        """
        user = self.request.user
        year, month = int(self.request.GET["year"]), int(self.request.GET["month"])

        yyyymm = f'{int(self.request.GET["year"])}{int(self.request.GET["month"]):02d}'
        self.queryset = Calendar.objects.filter(pk__in=user.permitted_calendar_id).schedules.filter(Q(start__year__lte=year) & Q(start__month__lte=month)).filter(Q(end__year__gte=year) & Q(end__month__gte=month))
        return super().get_queryset()

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
