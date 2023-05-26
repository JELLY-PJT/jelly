from django.urls import path
from . import views


app_name = 'groups'
urlpatterns = [
    path('', views.index, name='index'),
    # path('<int:group_pk>/', views.GroupDetail.as_view()),
]