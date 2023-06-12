from django.urls import path, include
from rest_framework.routers import DefaultRouter
from schedules import views

# Create a router and register our viewsets with it.
admin_router = DefaultRouter()
admin_router.register(r'schedules', views.ScheduleViewSet, basename="schedule")
admin_router.register(r'calendars', views.CalendarViewSet, basename="calendar")

calendarrouter = DefaultRouter()
calendarrouter.register(r'calendars', views.UserCalendarViewSet, basename="calendar")

schedulerouter = DefaultRouter()
schedulerouter.register(r'schedules', views.CalendarScheduleViewSet, basename="schedule")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('api/', include(admin_router.urls)),
    path('', include(calendarrouter.urls)),
    path('calendars/<int:calendar_id>/', include(schedulerouter.urls)),
]