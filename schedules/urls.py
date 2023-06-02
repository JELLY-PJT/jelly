from django.urls import path
from . import views

app_name = 'schedules'
urlpatterns = [
    path('create/', views.create, name='create'),
    path('today/', views.today, name='today'),
    path('thisweek/', views.thisweek, name='thisweek'),
    path('thismonth/', views.thismonth, name='thismonth'),
    path('month/<int:year>/<int:month>/', views.themonth, name='themonth'),
    path('day/<int:year>/<int:month>/<int:day>/', views.theday, name='theday'),
]
