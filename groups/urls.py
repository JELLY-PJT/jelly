from django.urls import path
from . import views


app_name = 'groups'
urlpatterns = [
    path('', views.index, name='index'),
    # path('<int:group_pk>/', views.GroupDetail.as_view()),
    path('<int:group_pk>/posts/', views.PostsList.as_view()),
    path('posts/<int:post_pk>/', views.PostDetail.as_view()),
]