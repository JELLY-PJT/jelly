from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Group, Post, PostImage, PostComment, PostEmote, Vote, VoteSelect
from .serializers import GroupSerializer
from diaries.models import Diary, DiaryShare
from .forms import GroupForm, PostForm, PostImageDeleteForm, PostCommentForm, VoteForm
from django.http import JsonResponse
from django.contrib import messages
from itertools import chain
from operator import attrgetter
from argon2 import PasswordHasher as ph
import json
from django.core.paginator import Paginator
from django.db.models import Prefetch, Count


# 사이트 인덱스 페이지
@login_required
def index(request):
    groups = request.user.user_groups.all()
    context = {
        'groups': groups,
    }
    return render(request, 'groups/index.html', context)


# 그룹 생성
@login_required
def group_create(request):
    form = GroupForm(request.POST, request.FILES)
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')

    if form.is_valid() and password1 == password2:
        group = form.save(commit=False)
        group.chief = request.user
        group.password = ph().hash(password1)  # 비밀번호 hashing해서 저장
        group.exp = 1
        group.level = 1
        group.save()
        group._calendar.create() # greate group calendar
        group.group_users.add(request.user)
        return redirect('groups:group_detail', group.pk)
    else:
        messages.error(request, '정보를 정확하게 입력하세요.')
        return redirect('groups:index')


# 그룹 레벨 이름 & 이미지
LEVEL = {
    1: {'name': '새싹', 'img': 'img/group_level/lv1_sprout.png', 'levelup_standard': 10},
    2: {'name': '풀잎', 'img': 'img/group_level/lv2_grass.png', 'levelup_standard': 30},
    3: {'name': '나무', 'img': 'img/group_level/lv3_tree.png', 'levelup_standard': 60},
    4: {'name': '개화', 'img': 'img/group_level/lv4_flower.png', 'levelup_standard': 100},
    5: {'name': '열매', 'img': 'img/group_level/lv5_fruit.png', 'levelup_standard': 150},
    6: {'name': '반달곰', 'img': 'img/group_level/lv6_bear.png', 'levelup_standard': 210},
    7: {'name': '판다', 'img': 'img/group_level/lv7_panda.png', 'levelup_standard': 280},
    8: {'name': '레서판다', 'img': 'img/group_level/lv8_lesser_panda.png', 'levelup_standard': 360},
    9: {'name': '유니콘', 'img': 'img/group_level/lv9_unicorn.png', 'levelup_standard': 450},
    10: {'name': '뿔 달린 유니콘', 'img': 'img/group_level/lv10_horn_unicorn.png', 'levelup_standard': 550},
    11: {'name': '날개 달린 유니콘', 'img': 'img/group_level/lv11_wing_unicorn.png', 'levelup_standard': 660},
}

# 그룹 경험치 추가 & 레벨업 관리
def exp_up(group_pk):
    group = Group.objects.get(pk=group_pk)
    group.exp += 1
    group.save()
    if group.exp/(len(group.group_users.all())**0.5) >= LEVEL[group.level]['levelup_standard']:
        group.level += 1
        group.save()


# 그룹 참가
def group_join(request, group_pk):
    group = Group.objects.get(pk=group_pk)

    if not request.user.is_authenticated:
        # 로그인 후 다시 group join url로 가도록 파라미터를 함께 보냄
        return redirect(f'/accounts/login/?next={request.path}')

    if group.group_users.filter(pk=request.user.pk).exists():
        return redirect('groups:group_detail', group.pk)

    if request.method == 'POST':
        jsonResponse = json.loads(request.body.decode('utf-8'))
        password = jsonResponse.get('password')

        try:
            ph().verify(group.password, password)
            group.group_users.add(request.user)
            exp_up(group_pk)
            return redirect('groups:group_detail', group.pk)
        except:
            messages.error(request, '암호가 일치하지 않습니다.')
            return JsonResponse({'message': '암호가 일치하지 않습니다.'})
    else:
        return render(request, 'groups/group_join.html', {'group': group,})


# 그룹 페이지 조회
@login_required
def group_detail(request, group_pk):
    group = Group.objects.prefetch_related('group_users').get(pk=group_pk)
    if not group.group_users.filter(pk=request.user.pk).exists():
        return redirect('groups:index')
    
    # 그룹 레벨 정보(이름, 이미지경로, 레벨업 기준)
    level_dict = LEVEL[group.level]
    group_exp = group.exp/(len(group.group_users.all())**0.5)
    
    if group.level > 1:
        group_exp -= float(LEVEL[group.level-1]['levelup_standard'])
        levelup_total = float(LEVEL[group.level]['levelup_standard']) - float(LEVEL[group.level-1]['levelup_standard'])
        levelup_percent = group_exp / levelup_total * 100
    else:
        levelup_total = 10
        levelup_percent = group_exp * 10

    
    # 공지로 등록된 post, vote 조회
    noticed_post = Post.objects.filter(group=group, is_notice=True)
    noticed_vote = Vote.objects.filter(group=group, is_notice=True)
    notices = list(chain(noticed_post, noticed_vote))
    notices.sort(key=attrgetter('created_at'), reverse=True)

    vote_form = VoteForm()

    # diary, post, vote 조회
    diaries = DiaryShare.objects.filter(group=group)
    posts = Post.objects.filter(group=group)
    votes = Vote.objects.filter(group=group)

    # diary, post, vote list에 담아 최신순 정렬 후 페이지네이션
    writings = list(chain(diaries, posts, votes))
    writings.sort(key=attrgetter('created_at'), reverse=True)
    page = request.GET.get('page', '1')
    per_page = 5
    pagination = Paginator(writings, per_page)
    page_objects = pagination.get_page(page)

    joined_vote = [selection.vote for selection in request.user.selections.all()]
    voter_cnt = {}
    for obj in page_objects:
        if obj.get_model_name() == 'vote':
            voter_cnt[obj.pk] = 0
            for option in obj.voteselect_set.all():
                voter_cnt[obj.pk] += option.select_users.count()

    context = {
        'group': group,
        'level_dict': level_dict,
        'group_exp': round(group_exp, 2),
        'levelup_total': round(levelup_total, 2),
        'levelup_percent': round(levelup_percent, 2),
        'notices': notices,
        'vote_form': vote_form,
        'writings': page_objects,
        'joined_vote': joined_vote,
        'voter_cnt': voter_cnt.items(),
    }
    return render(request, 'groups/group_detail.html', context)


# 그룹 설정 페이지
@login_required
def group_setting(request, group_pk):
    group = Group.objects.prefetch_related('group_users').get(pk=group_pk)
    if not group.group_users.filter(pk=request.user.pk).exists():
        return redirect('groups:index')
    
    if request.user != group.chief:
        return redirect('groups:group_detail', group.pk)
    
    form = GroupForm(instance=group)
    context = {
        'group': group,
        'form': form,
    }
    return render(request, 'groups/group_setting.html', context)


# 그룹 정보 수정
@login_required
def group_update(request, group_pk):
    group = Group.objects.prefetch_related('group_users').get(pk=group_pk)
    if not group.group_users.filter(pk=request.user.pk).exists():
        return redirect('groups:index')
    
    if request.user != group.chief:
        return redirect('groups:group_detail', group.pk)
    
    form = GroupForm(request.POST, instance=group)
    if form.is_valid():
        form.save()
        return redirect('groups:group_detail', group.pk)
    else:
        context = {
            'form': form,
        }
        messages.error(request, '정보를 정확하게 입력해주세요.')
        return render(request, 'groups/group_setting.html', context)


# 그룹 삭제
@login_required
def group_delete(request, group_pk):
    group = Group.objects.prefetch_related('group_users').get(pk=group_pk)
    if not group.group_users.filter(pk=request.user.pk).exists():
        return redirect('groups:index')
    
    if request.user != group.chief:
        return redirect('groups:group_detail', group.pk)
    
    group.delete()
    return redirect('groups:index')


# 그룹 암호 변경
@login_required
def password_update(request, group_pk):
    group = Group.objects.get(pk=group_pk)
    if not group.group_users.filter(pk=request.user.pk).exists():
        return redirect('groups:index')
    
    if request.user != group.chief:
        return redirect('groups:group_detail', group.pk)
    
    old_password = request.POST.get('old-password')
    password1 = request.POST.get('new-password1')
    password2 = request.POST.get('new-password2')

    try:
        ph().verify(group.password, old_password)
        if password1 == password2:
            group.password = ph().hash(password1)  # 비밀번호 hashing해서 저장
            group.save()
            return redirect('groups:group_detail', group.pk)
        else:
            messages.error(request, '비밀번호를 정확하게 입력하세요.')
            return redirect('groups:group_setting', group.pk)
    except:
        messages.error(request, '비밀번호를 정확하게 입력하세요.')
        return redirect('groups:group_setting', group.pk)


# 멤버 삭제
@login_required
def member_delete(request, group_pk, username):
    group = Group.objects.prefetch_related('group_users').get(pk=group_pk)
    if not group.group_users.filter(pk=request.user.pk).exists():
        return redirect('groups:index')
    
    if request.user != group.chief:
        return redirect('groups:group_detail', group.pk)
    
    member = get_user_model().objects.get(username=username)
    diaries = member.diary_set.all()
    for diary in diaries:
        diary.share.remove(group)
    posts = Post.objects.filter(user=member, group=group)
    for post in posts:
        post.delete()
    votes = Vote.objects.filter(user=member, group=group)
    for vote in votes:
        vote.delete()
        
    group.group_users.remove(member)
    return redirect('groups:group_setting', group.pk)


# 그룹 탈퇴
@login_required
def member_withdraw(request, group_pk):
    group = Group.objects.prefetch_related('group_users').get(pk=group_pk)
    if group.group_users.filter(pk=request.user.pk).exists():
        # 방장이면 탈퇴 못함
        if request.user == group.chief:
            return redirect('groups:group_detail', group.pk)
        else:
            diaries = request.user.diary_set.all()
            for diary in diaries:
                diary.share.remove(group)
            posts = Post.objects.filter(user=request.user, group=group)
            for post in posts:
                post.delete()
            votes = Vote.objects.filter(user=request.user, group=group)
            for vote in votes:
                vote.delete()

            group.group_users.remove(request.user)
    return redirect('groups:index')


# 방장 위임
@login_required
def chief_change(request, group_pk, username):
    group = Group.objects.prefetch_related('group_users').get(pk=group_pk)
    if not group.group_users.filter(pk=request.user.pk).exists():
        return redirect('groups:index')
    
    if request.user != group.chief:
        return redirect('groups:group_detail', group.pk)
    
    member = get_user_model().objects.get(username=username)
    group.chief = member
    return redirect('groups:group_detail', group.pk)


# post 생성
@login_required
def post_create(request, group_pk):
    group = Group.objects.get(pk=group_pk)
    if not group.group_users.filter(pk=request.user.pk).exists():
        return redirect('groups:index')
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        images = request.FILES.getlist('images')
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.group = group
            post.is_notice = False
            post.save()
            # 다중 이미지 저장
            for image in images:
                PostImage.objects.create(post=post, image=image)

            exp_up(group_pk)
            return redirect('groups:post_detail', group.pk, post.pk)
        else:
            messages.error(request, '내용을 올바르게 입력해주세요.')
    else:
        form = PostForm()
    context = {
        'group': group,
        'form': form,
    }
    return render(request, 'groups/post_create.html', context)


EMOTIONS = [
    {'label': '좋아요', 'value': 1},
    {'label': '최고에요', 'value': 2},
    {'label': '웃겨요', 'value': 3},
    {'label': '멋져요', 'value': 4},
    {'label': '슬퍼요', 'value': 5},
    {'label': '축하해요', 'value': 6},
]    # 1:👍 2:🥰 3:🤣 4:😲 5:😭 6:🥳

# post 조회
@login_required
def post_detail(request, group_pk, post_pk):
    group = Group.objects.get(pk=group_pk)
    if not group.group_users.filter(pk=request.user.pk).exists():
        return redirect('groups:index')
    
    post = Post.objects.get(pk=post_pk)
    comments = post.postcomment_set.all().order_by('-created_at')
    comment_form = PostCommentForm()
    # 조회수
    if not post.hits.filter(pk=request.user.pk).exists():
        post.hits.add(request.user)
    
    emotions = []
    for emotion in EMOTIONS:
        label = emotion['label']
        value = emotion['value']
        count = PostEmote.objects.filter(post=post, emotion=value).count()
        exist = PostEmote.objects.filter(post=post, emotion=value, user=request.user)
        emotions.append(
            {
                'label': label,
                'value': value,
                'count': count,
                'exist': exist,
            }
        )

    context = {
        'group': group,
        'post': post,
        'comment_form': comment_form,
        'comments': comments,
        'emotions': emotions,
    }
    return render(request, 'groups/post_detail.html', context)


# post 수정
@login_required
def post_update(request, group_pk, post_pk):
    group = Group.objects.get(pk=group_pk)
    if not group.group_users.filter(pk=request.user.pk).exists():
        return redirect('groups:index')

    post = Post.objects.get(pk=post_pk)
    if request.user != post.user:
        return redirect('groups:post_detail', group.pk, post.pk)

    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        image_delete_form = PostImageDeleteForm(request.POST)
        images = request.FILES.getlist('images')
        if post_form.is_valid() and image_delete_form.is_valid():
            post_form.save()
            # 선택한 이미지 삭제(save함수는 forms.py 참고)
            image_delete_form.save()
            # 다중 이미지 저장
            for image in images:
                PostImage.objects.create(post=post, image=image)
            return redirect('groups:post_detail', group.pk, post.pk)
        else:
            messages.error(request, '내용을 올바르게 입력해주세요.')
    else:
        post_form = PostForm(instance=post)
        image_delete_form = PostImageDeleteForm(instance=post)
    context = {
        'group': group,
        'post': post,
        'post_form': post_form,
        'image_delete_form': image_delete_form,
    }
    return render(request, 'groups/post_update.html', context)


# post 삭제
@login_required
def post_delete(request, group_pk, post_pk):
    group = Group.objects.get(pk=group_pk)
    if not group.group_users.filter(pk=request.user.pk).exists():
        return redirect('groups:index')
    
    post = Post.objects.get(pk=post_pk)
    if request.user != post.user:
        return redirect('groups:post_detail', group.pk, post.pk)
    
    post.delete()
    return redirect('groups:group_detail', group.pk)


# post 공지사항 등록/취소
@login_required
def notice_post(request, group_pk, post_pk):
    group = Group.objects.get(pk=group_pk)
    if not group.group_users.filter(pk=request.user.pk).exists():
        return redirect('groups:index')
    
    post = Post.objects.get(pk=post_pk)
    if post.is_notice:
        post.is_notice = False
        post.save()
    else:
        notice_cnt = len(Post.objects.filter(group=group, is_notice=True))
        notice_cnt += len(Vote.objects.filter(group=group, is_notice=True))
        if notice_cnt < 3:
            post.is_notice = True
            post.save()
        else:
            messages.info(request, '공지사항은 3개까지 등록 가능합니다. 기존의 공지를 삭제하고 다시 등록해주세요.')
    return redirect('groups:group_detail', group_pk)


# post 감정표현
@login_required
def emote(request, group_pk, post_pk, emotion):
    group = Group.objects.get(pk=group_pk)
    if not group.group_users.filter(pk=request.user.pk).exists():
        return redirect('groups:index')
    
    post = Post.objects.get(pk=post_pk)
    try:
        post_emotion = PostEmote.objects.get(post=post, user=request.user)
        if post_emotion.emotion != emotion:
            post_emotion.emotion = emotion
            post_emotion.save()
        else:
            post_emotion.delete()
    except PostEmote.DoesNotExist:
        PostEmote.objects.create(post=post, user=request.user, emotion=emotion)
    return redirect('groups:post_detail', group.pk, post.pk)


# 댓글 생성
@login_required
def comment_create(request, group_pk, post_pk):
    group = Group.objects.get(pk=group_pk)
    if not group.group_users.filter(pk=request.user.pk).exists():
        return redirect('groups:index')
    
    post = Post.objects.get(pk=post_pk)
    form = PostCommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = post
        comment.save()
        exp_up(group_pk)
    else:
        messages.error(request, '내용을 올바르게 입력해주세요.')
    return redirect('groups:post_detail', group.pk, post.pk)


# 댓글 수정
@login_required
def comment_update(request, group_pk, post_pk, comment_pk):
    group = Group.objects.get(pk=group_pk)
    if not group.group_users.filter(pk=request.user.pk).exists():
        return redirect('groups:index')
    
    comment = PostComment.objects.get(pk=comment_pk)

    if request.method == 'POST':
        form = PostCommentForm(request.POST, instance=comment)
        if form.is_valid():
            updated_comment = form.save(commit=False)
            updated_comment.save()

        context = {
            'content': updated_comment.content,
        }
        return JsonResponse(context)


# 댓글 삭제
@login_required
def comment_delete(request, group_pk, post_pk, comment_pk):
    group = Group.objects.get(pk=group_pk)
    if not group.group_users.filter(pk=request.user.pk).exists():
        return redirect('groups:index')
    
    comment = PostComment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('groups:post_detail', group.pk, post_pk)


def comment_like(request, group_pk, post_pk, comment_pk):
    group = Group.objects.get(pk=group_pk)
    if not group.group_users.filter(pk=request.user.pk).exists():
        return redirect('groups:index')
    comment = PostComment.objects.get(pk=comment_pk)

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


# 투표 생성
@login_required
def vote_create(request, group_pk):
    group = Group.objects.get(pk=group_pk)
    if not group.group_users.filter(pk=request.user.pk).exists():
        return redirect('groups:index')
    
    form = VoteForm(request.POST)
    options = request.POST.getlist('options')
    # 선택지 유효성 검사
    option_valid = True
    for option in options:
        test_option = option.replace(' ', '')
        if test_option == '':
            option_valid = False
    if form.is_valid() and option_valid:
        vote = form.save(commit=False)
        vote.user = request.user
        vote.group = group
        vote.is_notice = False
        vote.save()
        vote.hits.add(request.user)
        exp_up(group_pk)

        for option in options:
            VoteSelect.objects.create(vote=vote, content=option)
    else:
        messages.error(request, '내용을 올바르게 입력해주세요.')
    return redirect('groups:group_detail', group.pk)


# 사용자 투표 행사/취소
@login_required
def throw_vote(request, group_pk, vote_pk):
    group = Group.objects.get(pk=group_pk)
    if not group.group_users.filter(pk=request.user.pk).exists():
        return redirect('groups:index')

    vote = Vote.objects.get(pk=vote_pk)
    # js에서 만든 selected_list를 받아옴
    selected_options_json = request.POST.get('selected_list')
    if selected_options_json:
        selected_options = json.loads(selected_options_json)
    else:
        selected_options = []
    
    # 기존 투표 삭제 후 새로 저장
    for option in vote.voteselect_set.all():
        if option.select_users.filter(pk=request.user.pk).exists():
            option.select_users.remove(request.user)
    
    for option_id in selected_options:
        option = VoteSelect.objects.get(pk=option_id)
        option.select_users.add(request.user)

    return redirect('groups:group_detail', group.pk)


# vote is_addible이 True일 경우 멤버의 선택지 추가 기능
@login_required
def add_option(request, group_pk, vote_pk):
    group = Group.objects.get(pk=group_pk)
    if not group.group_users.filter(pk=request.user.pk).exists():
        return redirect('groups:index')
    
    vote = Vote.objects.get(pk=vote_pk)
    options = request.POST.getlist('options')
    # 선택지 유효성 검사
    option_valid = True
    for option in options:
        test_option = option.replace(' ', '')
        if test_option == '':
            option_valid = False
    
    if option_valid:
        for option in options:
            VoteSelect.objects.create(vote=vote, content=option)
    else:
        messages.error(request, '내용을 올바르게 입력해주세요.')
    return redirect('groups:group_detail', group.pk)


# vote 수정 form에 기존 정보 입력을 위해 JsonResponse로 js file로 데이터 넘겨주는 함수
@login_required
def get_vote(request, vote_pk):
    vote = Vote.objects.get(pk=vote_pk)
    options = [vote_option.content for vote_option in vote.voteselect_set.all()]
    context = {
        'id': vote.pk,
        'title': vote.title,
        'deadline': vote.deadline,
        'is_overlap': vote.is_overlap,
        'is_annony': vote.is_annony,
        'is_addible': vote.is_addible,
        'options': options,
    }
    return JsonResponse(context)


# 투표 수정
@login_required
def vote_update(request, group_pk, vote_pk):
    group = Group.objects.get(pk=group_pk)
    if not group.group_users.filter(pk=request.user.pk).exists():
        return redirect('groups:index')

    vote = Vote.objects.get(pk=vote_pk)
    form = VoteForm(request.POST, instance=vote)
    options = request.POST.getlist('options')
    # 선택지 유효성 검사
    option_valid = True
    for option in options:
        test_option = option.replace(' ', '')
        if test_option == '':
            option_valid = False
    
    if form.is_valid() and option_valid:
        form.save()

        # 기존 선택지 삭제
        for option in vote.voteselect_set.all():
            option.delete()
        # input 받은 선택지로 다시 저장
        for option in options:
            VoteSelect.objects.create(vote=vote, content=option)
    else:
        messages.error(request, '내용을 올바르게 입력해주세요.')
    return redirect('groups:group_detail', group.pk)


# 투표 삭제
@login_required
def vote_delete(request, group_pk, vote_pk):
    group = Group.objects.get(pk=group_pk)
    if not group.group_users.filter(pk=request.user.pk).exists():
        return redirect('groups:index')
    
    vote = Vote.objects.get(pk=vote_pk)
    if request.user == vote.user:
        vote.delete()
    return redirect('groups:group_detail', group.pk)


# vote 공지사항 등록/취소
@login_required
def notice_vote(request, group_pk, vote_pk):
    group = Group.objects.get(pk=group_pk)
    if not group.group_users.filter(pk=request.user.pk).exists():
        return redirect('groups:index')
    
    vote = Vote.objects.get(pk=vote_pk)
    if vote.is_notice:
        vote.is_notice = False
        vote.save()
    else:
        notice_cnt = len(Post.objects.filter(group=group, is_notice=True))
        notice_cnt += len(Vote.objects.filter(group=group, is_notice=True))
        if notice_cnt < 3:
            vote.is_notice = True
            vote.save()
        else:
            messages.info(request, '공지사항은 3개까지 등록 가능합니다. 기존의 공지를 삭제하고 다시 등록해주세요.')
    return redirect('groups:group_detail', group_pk)


# vote 조회수
@login_required
def vote_hits(request, vote_pk):
    vote = Vote.objects.get(pk=vote_pk)
    if not vote.hits.filter(pk=request.user.pk).exists():
        vote.hits.add(request.user)
    context = {
        'vote_hits': vote.hits.count()
    }
    return JsonResponse(context)


# group index 의 search function
@login_required
def group_search(request):
    if request.method == 'GET':
        q = request.GET['q'].strip()
        if q == "":
            groups = request.user.user_groups.all()
        else:
            groups = request.user.user_groups.filter(name__icontains=q)
        serializer = GroupSerializer(groups, many=True)
        return JsonResponse(serializer.data, safe=False)