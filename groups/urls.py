from django.urls import path, include
from schedules.urls import group_schedule_router
from . import views

app_name = 'groups'
urlpatterns = [
    path('', views.index, name='index'),
    # 그룹
    path('create/', views.group_create, name='group_create'),
    path('<int:group_pk>/join/', views.group_join, name='group_join'),
    path('<int:group_pk>/', views.group_detail, name='group_detail'),
    path('<int:group_pk>/setting/', views.group_setting, name='group_setting'),
    path('<int:group_pk>/update/', views.group_update, name='group_update'),
    path('<int:group_pk>/delete/', views.group_delete, name='group_delete'),
    path('<int:group_pk>/password_update/', views.password_update, name='password_update'),
    path('<int:group_pk>/members/withdraw/', views.member_withdraw, name='member_withdraw'), # 멤버 탈퇴(본인이)
    path('<int:group_pk>/members/<str:username>/delete/', views.member_delete, name='member_delete'), # 멤버 삭제(방장 권한)
    path('<int:group_pk>/chief/<str:username>/change/', views.chief_change, name='chief_change'), # 방장 위임
    # 게시글
    path('<int:group_pk>/posts/create/', views.post_create, name='post_create'),
    path('<int:group_pk>/posts/<int:post_pk>/', views.post_detail, name='post_detail'),
    path('<int:group_pk>/posts/<int:post_pk>/update/', views.post_update, name='post_update'),
    path('<int:group_pk>/posts/<int:post_pk>/delete/', views.post_delete, name='post_delete'),
    path('<int:group_pk>/posts/<int:post_pk>/emotes/<int:emotion>/', views.emote, name='emote'),
    path('<int:group_pk>/posts/<int:post_pk>/comment/create/', views.comment_create, name='comment_create'),
    path('<int:group_pk>/posts/<int:post_pk>/comment/<int:comment_pk>/update/', views.comment_update, name='comment_update'),
    path('<int:group_pk>/posts/<int:post_pk>/comment/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
    path('<int:group_pk>/posts/<int:post_pk>/comments/<int:comment_pk>/like/', views.comment_like, name='comment_like'),
    path('<int:group_pk>/posts/<int:post_pk>/notice/', views.notice_post, name='notice_post'),
    # 투표
    path('<int:group_pk>/votes/create/', views.vote_create, name='vote_create'),
    path('votes/<int:vote_pk>/', views.get_vote, name='get_vote'),
    path('<int:group_pk>/votes/<int:vote_pk>/throw/', views.throw_vote, name='throw_vote'),
    path('<int:group_pk>/votes/<int:vote_pk>/add_option/', views.add_option, name='add_option'),
    path('<int:group_pk>/votes/<int:vote_pk>/update/', views.vote_update, name='vote_update'),
    path('<int:group_pk>/votes/<int:vote_pk>/delete/', views.vote_delete, name='vote_delete'),
    path('<int:group_pk>/votes/<int:vote_pk>/notice/', views.notice_vote, name='notice_vote'),
    path('votes/<int:vote_pk>/hits/', views.vote_hits, name='vote_hits'),
    path('search/', views.group_search, name='group_search'),
    path('<int:group_pk>/calendars/', include(group_schedule_router.urls)),
]
