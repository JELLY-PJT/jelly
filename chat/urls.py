# chat/urls.py
from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("<int:group_pk>/", views.group_chat, name="group_chat"),
]