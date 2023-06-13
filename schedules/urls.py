from django.urls import path, include
from rest_framework.routers import DefaultRouter
from schedules import views

# Create a router and register our viewsets with it.
admin_router = DefaultRouter()
admin_router.register(r'schedules', views.ScheduleViewSet, basename="schedule")
admin_router.register(r'calendars', views.CalendarViewSet, basename="calendar")

user_schedule_router = DefaultRouter()
user_schedule_router.register(r'schedules', views.UserScheduleViewSet, basename="user_schedule")

group_schedule_router = DefaultRouter()
group_schedule_router.register(r'schedules', views.GroupScheduleViewSet, basename="group_schedule")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('api/', include(admin_router.urls)),
    path('', include(user_schedule_router.urls)),
]