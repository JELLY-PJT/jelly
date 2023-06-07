from django.urls import path, include
from rest_framework.routers import DefaultRouter
from schedules import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'schedules', views.ScheduleViewSet, basename="schedule")
router.register(r'calendars', views.CalendarViewSet, basename="calendar")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]