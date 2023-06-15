from django.urls import path, include
from . import views
from schedules.urls import user_schedule_router 

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('delete/', views.delete, name='delete'),
    path('update/', views.update, name='update'),
    path('password/', views.change_password, name='change_password'),
    path('profile/<username>/', views.profile, name='profile'),
    path('profile/<username>/post/', views.profile, name='profile_share'),
    path('profile/<username>/share/', views.profile, name='profile_share'),
    path('profile/<username>/calendar/', views.profile, name='profile_share'),
    path('profile/<username>/calendar/schedules/', include(user_schedule_router.urls)),
]
