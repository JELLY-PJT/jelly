# chat/views.py
from django.shortcuts import render, get_object_or_404, get_list_or_404
from groups.models import Group
from .models import Message


def index(request):
    return render(request, "chat/index.html")


# 요청자가 그룹원인지 확인 필요.
def group_chat(request, group_pk):
    group = get_object_or_404(Group, pk=group_pk)
    messages = Message.objects.filter(group=group)
    me_pk = request.user.pk
    context = {
        'group': group,
        'group_pk': group_pk,
        'messages': messages,
        'me_pk': me_pk,
    }
    return render(request, "chat/room.html", context)