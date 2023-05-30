from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Diary, DiaryComment, DiaryShare
from .forms import DiaryForm, DiaryCommentForm
from groups.models import Group
from django.http import JsonResponse


# Create your views here.
def index(request):
    diaries = Diary.objects.filter(user=request.user)
    context = {
        'diaries': diaries,
    }
    return render(request, 'diaries/index.html', context)


def create(request):
    if request.method == 'POST':
        form = DiaryForm(request.POST)
        if form.is_valid():
            diary = form.save(commit=False)
            diary.user = request.user
            diary.save()
            return redirect('diaries:detail', diary.pk)
    else:
        form = DiaryForm()
    context = {
        'form': form,
    }
    return render(request, 'diaries/create.html', context)


def detail(request, diary_pk):
    diary = Diary.objects.get(pk=diary_pk)
    if request.user == diary.user:
        context = {
            'diary': diary
        }
        return render(request, 'diaries/diary.html', context)
    return redirect('diaries:index')


def update(request, diary_pk):
    diary = Diary.objects.get(pk=diary_pk)
    if request.user == diary.user:
        if request.method == 'POST':
            form = DiaryForm(request.POST, instance=diary)
            if form.is_valid():
                form.save()
                return redirect('diaries:detail', diary.pk)
        else:
            form = DiaryForm(instance=diary)
        context = {
            'form': form,
        }
        return render(request, 'diaries/update.html', context)
    return redirect('diaries:index')


def delete(request, diary_pk):
    diary = Diary.objects.get(pk=diary_pk)
    if request.user == diary.user:
        diary.delete()
    return redirect('diaries:index')


# 그룹에 공유된 diary
# emotes 구현 필요
def group_detail(request, group_pk, diary_pk):
    group = get_object_or_404(Group, pk=group_pk)
    diary_share = get_object_or_404(DiaryShare, group=group, diary_pk=diary_pk)
    diary = diary_share.diary
    comments = diary.diarycomment_set.filter(group=group)

    if group.users.filter(pk=request.user.pk).exists():
        comment_form = DiaryCommentForm()
        context = {
            'diary': diary,
            'comment_form': comment_form,
            'comments': comments,
        }
        return render(request, 'diaries/group_detail.html', context)
    return redirect('diaries:index')


def share(request, group_pk, diary_pk):
    group = get_object_or_404(Group, pk=group_pk)
    diary = get_object_or_404(Diary, pk=diary_pk)

    if DiaryShare.objects.filter(group=group, diary=diary).exists:
        return redirect('diaries:detail', diary_pk)
    
    diary_share = DiaryShare.objects.create(group=group, diary=diary)
    return redirect('diaries:group_detail', group_pk, diary_pk)


def unshare(request, group_pk, diary_pk):
    group = get_object_or_404(Group, pk=group_pk)
    diary_share = get_object_or_404(DiaryShare, group=group, diary_pk=diary_pk)
    diary = diary_share.diary
    if request.user == diary.user:
        diary.share.remove(group)
        return redirect('diaries:index')
    return redirect('diaries:group_detail', group_pk=group_pk, diary_pk=diary_pk)


# request.user가 그룹 내에 존재 하는지.
# 그룹 공유된 diary detail 어디서 처리할지
def comment_create(request, group_pk, diary_pk):
    group = get_object_or_404(Group, pk=group_pk)

    if group.users.filter(pk=request.user.pk).exists():
        diary_share = get_object_or_404(DiaryShare, group=group, diary_pk=diary_pk)
        form = DiaryCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.diary = diary_share.diary
            comment.user = request.user
            comment.save()
            messages.success(request, "댓글이 작성되었습니다.")
            # return JsonResponse({'success': True})

        return redirect('diaries:group_detail', group_pk=group_pk, diary_pk=diary_pk)
        # return JsonResponse({'success': False, 'errors': comment_form.errors})
    else:
        messages.error(request, "올바른 접근이 아닙니다.")
        return redirect('diaries:index')
    

def comment_update(request, group_pk, diary_pk, comment_pk):
    group = get_object_or_404(Group, pk=group_pk)
    comment = get_object_or_404(DiaryComment, pk=comment_pk)

    if comment.user != request.user:
        messages.error(request, "올바른 접근이 아닙니다.")
        return redirect('diaries:group_detail', group_pk=group_pk, diary_pk=diary_pk)

    if group.users.filter(pk=request.user.pk).exists():
        # 공유된 게시물인지 확인 get_object_or_404말고 다른 방법 있는지 체크
        diary_share = get_object_or_404(DiaryShare, group=group, diary_pk=diary_pk)
        if request.method == 'POST':
            form = DiaryCommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                messages.success(request, "댓글이 수정되었습니다.")
                return redirect('diaries:group_detail', group_pk=group_pk, diary_pk=diary_pk)
        else:
            form = DiaryCommentForm(instance=comment)
        context = {
            'form': form,
        }
        return render(request, 'comment_create.html', context)
    else:
        messages.error(request, "올바른 접근이 아닙니다.")
        return redirect('diaries:index')
    

def comment_delete(request, group_pk, diary_pk, comment_pk):
    group = get_object_or_404(Group, pk=group_pk)
    comment = get_object_or_404(DiaryComment, pk=comment_pk)
    
    if group.users.filter(pk=request.user.pk).exists():
        diary_share = get_object_or_404(DiaryShare, group=group, diary_pk=diary_pk)
        if request.user == comment.user:
            comment.delete()
            messages.success(request, "댓글이 삭제되었습니다.")
        return redirect('diaries:group_detail', group_pk=group_pk, diary_pk=diary_pk)
    else:
        messages.error(request, "올바른 접근이 아닙니다.")
        return redirect('diaries:index')


def comment_like(request, group_pk, diary_pk, comment_pk):
    group = get_object_or_404(Group, pk=group_pk)
    comment = get_object_or_404(DiaryComment, pk=comment_pk)
    if comment.like_users.filter(pk=request.user.pk).exists():
        comment.like_users.remove(request.user)
    else:
        comment.like_users.add(request.user)
    return redirect('diaries:group_detail', group_pk=group_pk, diary_pk=diary_pk)