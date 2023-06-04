from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Diary, DiaryComment, DiaryShare, DiaryEmote
from .forms import DiaryForm, DiaryCommentForm
from groups.models import Group
from django.http import JsonResponse

EMOTIONS = [
    {'label': '좋아요', 'value': 1},
    {'label': '최고에요', 'value': 2},
    {'label': '웃겨요', 'value': 3},
    {'label': '멋져요', 'value': 4},
    {'label': '슬퍼요', 'value': 5},
    {'label': '축하해요', 'value': 6},
]    # 1:👍 2:🥰 3:🤣 4:😲 5:😭 6:🥳

# 개인 다이어리 인덱스
def index(request):
    diaries = Diary.objects.filter(user=request.user)
    context = {
        'diaries': diaries,
    }
    return render(request, 'diaries/index.html', context)


# 개인 다이어리 작성
def create(request):
    if request.method == 'POST':
        form = DiaryForm(data=request.POST, files=request.FILES)
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


# 개인 다이어리 조회 / 공유했다면 각 그룹에 달린 감정, 댓글 표시(아직 미구현)
def detail(request, diary_pk):
    diary = Diary.objects.get(pk=diary_pk)
    if request.user == diary.user:
        context = {
            'diary': diary
        }
        return render(request, 'diaries/diary.html', context)
    return redirect('diaries:index')


# 개인 다이어리 수정
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
            'diary': diary,
        }
        return render(request, 'diaries/update.html', context)
    return redirect('diaries:index')


# 개인 다이어리 삭제
def delete(request, diary_pk):
    diary = Diary.objects.get(pk=diary_pk)
    if request.user == diary.user:
        diary.delete()
    return redirect('diaries:index')


# 그룹에 공유된 다이어리 디테일 / 감정, 댓글작성 가능
# emotes 구현 필요
def group_detail(request, group_pk, diary_pk):
    group = get_object_or_404(Group, pk=group_pk)
    diary = get_object_or_404(Diary, pk=diary_pk)
    diary_share = get_object_or_404(DiaryShare, group=group, diary=diary)
    comments = diary_share.diarycomment_set.all()

    emotions = []
    for emotion in EMOTIONS:
        label = emotion['label']
        value = emotion['value']
        count = DiaryEmote.objects.filter(share=diary_share, emotion=value).count()
        exist = DiaryEmote.objects.filter(share=diary_share, emotion=value, user=request.user)
        emotions.append(
            {
                'label': label,
                'value': value,
                'count': count,
                'exist': exist,
            }
        )

    if group.group_users.filter(pk=request.user.pk).exists():
        comment_form = DiaryCommentForm()
        context = {
            'diary': diary,
            'diary_share': diary_share,
            'emotions': emotions,
            'group': group,
            'comment_form': comment_form,
            'comments': comments,
        }
        return render(request, 'diaries/group_detail.html', context)
    return redirect('diaries:index')


# 개인 다이어리를 원하는 그룹에 공유
def share(request, group_pk, diary_pk):
    group = get_object_or_404(Group, pk=group_pk)
    diary = get_object_or_404(Diary, pk=diary_pk)

    if DiaryShare.objects.filter(group=group, diary=diary).exists():
        return redirect('diaries:detail', diary_pk)
    
    diary_share = DiaryShare.objects.create(group=group, diary=diary)
    return redirect('diaries:group_detail', group_pk, diary_pk)


# 공유된 다이어리의 공유 취소
def unshare(request, group_pk, diary_pk):
    group = get_object_or_404(Group, pk=group_pk)
    diary = get_object_or_404(Diary, pk=diary_pk)
    diary_share = get_object_or_404(DiaryShare, group=group, diary=diary)
    if request.user == diary.user:
        diary.share.remove(group)
        return redirect('diaries:index')
    return redirect('diaries:group_detail', group_pk=group_pk, diary_pk=diary_pk)


def emotes(request, group_pk, diary_pk, emotion):
    group = get_object_or_404(Group, pk=group_pk)
    diary = get_object_or_404(Diary, pk=diary_pk)
    diary_share = get_object_or_404(DiaryShare, group=group, diary=diary)

    try:
        diary_emote = DiaryEmote.objects.get(share=diary_share, user=request.user)
        if diary_emote.emotion != emotion:
            diary_emote.emotion = emotion
            diary_emote.save()
        else:
            diary_emote.delete()
    except DiaryEmote.DoesNotExist:
        DiaryEmote.objects.create(share=diary_share, user=request.user, emotion=emotion)
    return redirect('diaries:group_detail', group_pk=group_pk, diary_pk=diary_pk)


# 공유된 다이어리에 댓글 작성
def comment_create(request, group_pk, diary_pk):
    group = get_object_or_404(Group, pk=group_pk)
    diary = get_object_or_404(Diary, pk=diary_pk)

    if group.group_users.filter(pk=request.user.pk).exists():
        diary_share = get_object_or_404(DiaryShare, group=group, diary=diary)
        form = DiaryCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.share = diary_share
            comment.user = request.user
            comment.save()
            messages.success(request, "댓글이 작성되었습니다.")
            # return JsonResponse({'success': True})

        return redirect('diaries:group_detail', group_pk=group_pk, diary_pk=diary_pk)
        # return JsonResponse({'success': False, 'errors': comment_form.errors})
    else:
        messages.error(request, "올바른 접근이 아닙니다.")
        return redirect('diaries:index')
    

# 공유된 다이어리 댓글 수정
def comment_update(request, group_pk, diary_pk, comment_pk):
    group = get_object_or_404(Group, pk=group_pk)
    diary = get_object_or_404(Diary, pk=diary_pk)
    comment = get_object_or_404(DiaryComment, pk=comment_pk)

    if comment.user != request.user:
        messages.error(request, "올바른 접근이 아닙니다.")
        return redirect('diaries:group_detail', group_pk=group_pk, diary_pk=diary_pk)

    if group.group_users.filter(pk=request.user.pk).exists():
        # 공유된 게시물인지 확인 get_object_or_404말고 다른 방법 있는지 체크
        
        diary_share = get_object_or_404(DiaryShare, group=group, diary=diary)
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
    

# 공유된 다이어리 댓글 삭제
def comment_delete(request, group_pk, diary_pk, comment_pk):
    group = get_object_or_404(Group, pk=group_pk)
    diary = get_object_or_404(Diary, pk=diary_pk)
    comment = get_object_or_404(DiaryComment, pk=comment_pk)
    
    if group.group_users.filter(pk=request.user.pk).exists():
        diary_share = get_object_or_404(DiaryShare, group=group, diary=diary)
        if request.user == comment.user:
            comment.delete()
            messages.success(request, "댓글이 삭제되었습니다.")
        return redirect('diaries:group_detail', group_pk=group_pk, diary_pk=diary_pk)
    else:
        messages.error(request, "올바른 접근이 아닙니다.")
        return redirect('diaries:index')


# 공유된 다이어리 댓글 좋아요(비동기처리)
def comment_like(request, group_pk, diary_pk, comment_pk):
    group = get_object_or_404(Group, pk=group_pk)
    comment = get_object_or_404(DiaryComment, pk=comment_pk)
    if comment.like_users.filter(pk=request.user.pk).exists():
        comment.like_users.remove(request.user)
        is_liked = False
    else:
        comment.like_users.add(request.user)
        is_liked = True

    context = {
        'is_liked': is_liked,
        'comment_like_users': comment.like_users.count(),
    }
    return JsonResponse(context)