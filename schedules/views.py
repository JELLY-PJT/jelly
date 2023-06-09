"""
for MVT pattern
"""
from django.shortcuts import render, redirect
from .models import *
"""
for DRF viewsets
"""
from rest_framework import viewsets
from django.db.models import Q
from .serializers import *
"""
for view based authentication scheme
"""
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
"""
lookups keyword : field__lookuptype=value
"""

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

class CalendarScheduleViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ScheduleSerializer
    def get_queryset(self):
        """
        현재 calendar의 모든 schedule을 list
        """
        q = self.kwargs
        calendar = Calendar.objects.get(id=q['calendar_id'])
        queryset = calendar.schedules.all()
        return queryset

class ScheduleViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer    

class CalendarViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer
