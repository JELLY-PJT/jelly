from django.urls import path
from . import views

appname = 'diaries'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:diary_pk>/', views.detail, name='detail'),
    path('<int:diary_pk>/update/', views.update, name='update'),
    path('<int:diary_pk>/delete/', views.delete, name='delete'),
    path('<int:group_pk>/<int:diary_pk>/', views.group_detail, name='group_detail'),
    path('<int:group_pk>/<int:diary_pk>/share/', views.share, name='share'),
    path('<int:group_pk>/<int:diary_pk>/unshare/', views.unshare, name='unshare'),
    # path('<int:group_pk>/<int:diary_pk>/emotes/<int:emotion>/', views.emotes, name='emotes'),
    path('<int:group_pk>/<int:diary_pk>/comment_create/', views.comment_create, name='comment_create'),
    path('<int:group_pk>/<int:diary_pk>/comments/<int:comment_pk>/update/', views.comment_update, name='DiaryCommentDetail'),
    path('<int:group_pk>/<int:diary_pk>/comments/<int:comment_pk>/delete/', views.comment_delete, name='DiaryCommentDetail'),
    path('<int:group_pk>/<int:diary_pk>/comments/<int:comment_pk>/like/', views.comment_like, name='comment_like'),
]