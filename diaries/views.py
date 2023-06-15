from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Diary, DiaryComment, DiaryShare, DiaryEmote
from .forms import DiaryForm, DiaryCommentForm
from groups.models import Group
from django.http import JsonResponse
from bs4 import BeautifulSoup
from django.db.models import Q

EMOTIONS = [
    {'label': '좋아요', 'value': 1},
    {'label': '최고에요', 'value': 2},
    {'label': '웃겨요', 'value': 3},
    {'label': '멋져요', 'value': 4},
    {'label': '슬퍼요', 'value': 5},
    {'label': '축하해요', 'value': 6},
]    # 1:👍 2:🥰 3:🤣 4:😲 5:😭 6:🥳

# 개인 다이어리 인덱스
@login_required
def index(request):
    diaries = Diary.objects.filter(user=request.user)
    context = {
        'diaries': diaries,
    }
    return render(request, 'diaries/index.html', context)


# 개인 다이어리 작성
@login_required
def create(request):
    if request.method == 'POST':
        form = DiaryForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            diary = form.save(commit=False)
            diary.user = request.user

            if not diary.thumbnail:  # thumbnail 필드가 비어있는 경우에만 처리
                # Diary 객체의 content 필드에 이미지 태그가 있는지 확인
                if '<img' in diary.content:
                    soup = BeautifulSoup(diary.content, 'html.parser')
                    img_tag = soup.find('img')
                    print(img_tag)
                    if img_tag:
                        first_img_url = img_tag['src']
                        diary.thumbnail = first_img_url
            diary.save()
            return redirect('diaries:detail', diary.pk)
        else:
            messages.error(request, '내용을 올바르게 입력해주세요.')
    else:
        form = DiaryForm()
    context = {
        'form': form,
    }
    return render(request, 'diaries/create.html', context)


# 개인 다이어리 조회 / 공유했다면 각 그룹에 달린 감정, 댓글 표시
@login_required
def detail(request, diary_pk):
    diary = get_object_or_404(Diary, pk=diary_pk)
    shares = DiaryShare.objects.filter(diary=diary).order_by('group')

    reactions = []
    group_emotions = [] # 각 그룹별 emotions(인덱스로 구분)
    group_comments = [] # 각 그룹별 댓글(인덱스로 구분)

    for share in shares:
        emotions = []
        for emotion in EMOTIONS:
            label = emotion['label']
            value = emotion['value']
            count = DiaryEmote.objects.filter(share=share, emotion=value).count()
            emotions.append(
                {
                    'label': label,
                    'value': value,
                    'count': count,
                }
            )
        comments = share.diarycomment_set.all()
        emote_count = share.diaryemote_set.all().count()
        group_emotions = emotions
        group_comments = comments
        reactions.append([share.group, emote_count, group_emotions, group_comments])

    if request.user == diary.user:
        context = {
            'diary': diary,
            'shares': shares,
            'group_emotions': group_emotions,
            'group_comments': group_comments,
            'reactions': reactions,
        }
        return render(request, 'diaries/diary.html', context)
    return redirect('diaries:index')


# 개인 다이어리 수정
@login_required
def update(request, diary_pk):
    diary = get_object_or_404(Diary, pk=diary_pk)
    if request.user == diary.user:
        if request.method == 'POST':
            form = DiaryForm(request.POST, instance=diary)
            if form.is_valid():
                form.save()
                return redirect('diaries:detail', diary.pk)
            else:
                messages.error(request, '내용을 올바르게 입력해주세요.')
        else:
            form = DiaryForm(instance=diary)
        context = {
            'form': form,
            'diary': diary,
        }
        return render(request, 'diaries/update.html', context)
    return redirect('diaries:index')


# 개인 다이어리 삭제
@login_required
def delete(request, diary_pk):
    diary = get_object_or_404(Diary, pk=diary_pk)
    if request.user == diary.user:
        diary.delete()
    return redirect('accounts:profile', request.user)


# 그룹에 공유된 다이어리 디테일 / 감정, 댓글작성 가능
@login_required
def group_detail(request, group_pk, diary_pk):
    group = get_object_or_404(Group, pk=group_pk)
    diary = get_object_or_404(Diary, pk=diary_pk)
    diary_share = get_object_or_404(DiaryShare, group=group, diary=diary)
    comments = diary_share.diarycomment_set.all()

    if not diary.hit.filter(pk=request.user.pk).exists():
        diary.hit.add(request.user)

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


# 그룹 레벨 이름 & 이미지
LEVEL = {
    1: {'name': '새싹', 'img': 'img/group_level/lv1_sprout.png', 'levelup_standard': 10},
    2: {'name': '잔디', 'img': 'img/group_level/lv2_grass.png', 'levelup_standard': 30},
    3: {'name': '나무', 'img': 'img/group_level/lv3_tree.png', 'levelup_standard': 60},
    4: {'name': '개화', 'img': 'img/group_level/lv4_flower.png', 'levelup_standard': 100},
    5: {'name': '열매', 'img': 'img/group_level/lv5_fruit.png', 'levelup_standard': 150},
    6: {'name': '반달곰', 'img': 'img/group_level/lv6_bear.png', 'levelup_standard': 210},
    7: {'name': '판다', 'img': 'img/group_level/lv7_panda.png', 'levelup_standard': 280},
    # 8: {'name': '레서판다', 'img': 'img/group_level/lv8_lesser_panda.png', 'levelup_standard': 360},
    # 9: {'name': '유니콘', 'img': 'img/group_level/lv9_unicorn.png', 'levelup_standard': 450},
    # 10: {'name': '뿔 달린 유니콘', 'img': 'img/group_level/lv10_horn_unicorn.png', 'levelup_standard': 550},
    # 11: {'name': '날개 달린 유니콘', 'img': 'img/group_level/lv11_wing_unicorn.png', 'levelup_standard': 660},
}

# 그룹 경험치 추가 & 레벨업 관리
def exp_up(group_pk):
    group = Group.objects.get(pk=group_pk)
    group.exp += 1
    group.save()
    if group.exp/(len(group.group_users.all())**0.5) >= LEVEL[group.level]['levelup_standard'] and group.level < 7:
        group.level += 1
        group.save()


# 개인 다이어리를 원하는 그룹에 공유
def share(request, group_pk, diary_pk):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    group = get_object_or_404(Group, pk=group_pk)
    if group.group_users.filter(pk=request.user.pk).exists():
        diary = get_object_or_404(Diary, pk=diary_pk)

        if DiaryShare.objects.filter(group=group, diary=diary).exists():
            return redirect('diaries:detail', diary_pk)
        
        diary_share = DiaryShare.objects.create(group=group, diary=diary)
        exp_up(group_pk)
        return redirect('diaries:group_detail', group_pk=group_pk, diary_pk=diary_pk)
    else:
        messages.error(request, "올바른 접근이 아닙니다.")
        return redirect('accounts:profile', request.user.username)


# 공유된 다이어리의 공유 취소
def unshare(request, group_pk, diary_pk):
    group = get_object_or_404(Group, pk=group_pk)
    diary = get_object_or_404(Diary, pk=diary_pk)
    diary_share = get_object_or_404(DiaryShare, group=group, diary=diary)
    if request.user == diary.user:
        diary.share.remove(group)
        return redirect('accounts:profile', request.user)
    return redirect('diaries:group_detail', group_pk=group_pk, diary_pk=diary_pk)


@login_required
def emotes(request, group_pk, diary_pk, emotion):
    group = get_object_or_404(Group, pk=group_pk)
    diary = get_object_or_404(Diary, pk=diary_pk)
    diary_share = get_object_or_404(DiaryShare, group=group, diary=diary)

    try:
        diary_emote = DiaryEmote.objects.get(share=diary_share, user=request.user)
        if diary_emote.emotion != emotion:
            diary_emote.emotion = emotion
            diary_emote.save()
            delete = False
            
        else:
            diary_emote.delete()
            delete = True

        context = {
            'delete': delete,
        }
        return JsonResponse(context)
    except DiaryEmote.DoesNotExist:
        DiaryEmote.objects.create(share=diary_share, user=request.user, emotion=emotion)
    return redirect('diaries:group_detail', group_pk=group_pk, diary_pk=diary_pk)


# 공유된 다이어리에 댓글 작성
@login_required
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
            exp_up(group_pk)
            # return JsonResponse({'success': True})

        return redirect('diaries:group_detail', group_pk=group_pk, diary_pk=diary_pk)
        # return JsonResponse({'success': False, 'errors': comment_form.errors})
    else:
        messages.error(request, "올바른 접근이 아닙니다.")
        return redirect('diaries:index')
    

# 공유된 다이어리 댓글 수정
@login_required
def comment_update(request, group_pk, diary_pk, comment_pk):
    group = get_object_or_404(Group, pk=group_pk)
    diary = get_object_or_404(Diary, pk=diary_pk)
    comment = get_object_or_404(DiaryComment, pk=comment_pk)

    if comment.user != request.user:
        messages.error(request, "올바른 접근이 아닙니다.")
        return redirect('diaries:group_detail', group_pk=group_pk, diary_pk=diary_pk)

    if group.group_users.filter(pk=request.user.pk).exists():
        
        diary_share = get_object_or_404(DiaryShare, group=group, diary=diary)
        if request.method == 'POST':
            form = DiaryCommentForm(request.POST, instance=comment)
            if form.is_valid():
                updated_comment = form.save(commit=False)
                updated_comment.save()

                context = {
                    'content': updated_comment.comment,
                }
                return JsonResponse(context)
        # else:
        #     form = DiaryCommentForm(instance=comment)
        # context = {
        #     'form': form,
        # }
        # return JsonResponse(context)
    else:
        messages.error(request, "올바른 접근이 아닙니다.")
        return redirect('diaries:index')
    

# 공유된 다이어리 댓글 삭제
@login_required
def comment_delete(request, group_pk, diary_pk, comment_pk):
    group = get_object_or_404(Group, pk=group_pk)
    diary = get_object_or_404(Diary, pk=diary_pk)
    comment = get_object_or_404(DiaryComment, pk=comment_pk)
    
    if group.group_users.filter(pk=request.user.pk).exists():
        diary_share = get_object_or_404(DiaryShare, group=group, diary=diary)
        if request.user == comment.user:
            comment.delete()
        return redirect('diaries:group_detail', group_pk=group_pk, diary_pk=diary_pk)
    else:
        messages.error(request, "올바른 접근이 아닙니다.")
        return redirect('diaries:index')


# 공유된 다이어리 댓글 좋아요(비동기처리)
@login_required
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