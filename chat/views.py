# chat/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from groups.models import Group
from .models import Message


def index(request):
    return render(request, "chat/index.html")


@login_required
def group_chat(request, group_pk):
    user = request.user
    group = get_object_or_404(Group, pk=group_pk)
    if group.group_users.filter(pk=request.user.pk).exists():
        messages = Message.objects.filter(group=group).order_by('-pk')[:30][::-1]

        context = {
            'group': group,
            'group_pk': group_pk,
            'messages': messages,
        }
        return render(request, "chat/room.html", context)
    else:
        messages.error(request, "올바른 접근이 아닙니다.")
        return redirect('accounts:profile', user.username)