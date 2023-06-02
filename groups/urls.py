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
    path('<int:group_pk>/posts/<int:post_pk>/emotes/<int:emotion>/', views.emote, name='emote'),
    path('<int:group_pk>/posts/<int:post_pk>/comment/create/', views.comment_create, name='comment_create'),
    path('<int:group_pk>/posts/<int:post_pk>/comment/<int:comment_pk>/update/', views.comment_update, name='comment_update'),
    path('<int:group_pk>/posts/<int:post_pk>/comment/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
    path('<int:group_pk>/votes/create/', views.vote_create, name='vote_create'),
    path('<int:group_pk>/votes/<int:vote_pk>/throw/<int:option_pk>/', views.throw_vote, name='throw_vote'),
]