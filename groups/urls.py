from django.urls import path
from . import views


app_name = 'groups'
urlpatterns = [
    path('', views.index, name='index'),
    path('group_create/', views.group_create, name='group_create'),
    path('<int:group_pk>/', views.group_detail, name='group_detail'),
    # path('<int:group_pk>/posts/', views.PostsList.as_view()),
    # path('posts/<int:post_pk>/', views.PostDetail.as_view()),
]