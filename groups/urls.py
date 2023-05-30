from django.urls import path
from . import views


app_name = 'groups'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.group_create, name='group_create'),
    path('<int:group_pk>/', views.group_detail, name='group_detail'),
    path('<int:group_pk>/posts/create/', views.post_create, name='post_create'),
    path('<int:group_pk>/posts/<int:post_pk>/', views.post_detail, name='post_detail'),
    path('<int:group_pk>/posts/<int:post_pk>/update/', views.post_update, name='post_update'),
    path('<int:group_pk>/posts/<int:post_pk>/delete/', views.post_delete, name='post_delete'),
    # path('posts/<int:post_pk>/', views.PostDetail.as_view()),
]