from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Group, Post, PostImage, PostComment, PostEmote, Vote, VoteSelect
from diaries.models import Diary, DiaryShare
from .forms import GroupForm, PostForm, PostImageDeleteForm, PostCommentForm, VoteForm
from django.http import JsonResponse
from django.contrib import messages
from itertools import chain
from operator import attrgetter
from django.db.models import Prefetch


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
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.chief = request.user
            group.save()
            group.group_users.add(request.user)
            return redirect('groups:group_detail', group.pk)
    else:
        form = GroupForm()
    context = {
        'form': form,
    }
    return render(request, 'groups/group_create.html', context)


# 그룹 페이지 조회
@login_required
def group_detail(request, group_pk):
    group = Group.objects.prefetch_related('group_users').get(pk=group_pk)
    if not group.group_users.filter(pk=request.user.pk).exists():
        return redirect('groups:index')
    
    # 공지로 등록된 post, vote 조회
    noticed_post = Post.objects.filter(group=group, is_notice=True)
    noticed_vote = Vote.objects.filter(group=group, is_notice=True)
    notices = list(chain(noticed_post, noticed_vote))
    notices.sort(key=attrgetter('created_at'), reverse=True)

    vote_form = VoteForm()

    # diary, post, vote 조회
    shared_diaries = DiaryShare.objects.filter(group=group)
    shared_diary_id = [obj.pk for obj in shared_diaries]
    diaries = Diary.objects.filter(pk__in=shared_diary_id)
    posts = Post.objects.filter(group=group)
    votes = Vote.objects.filter(group=group)
    vote_exist = {}
    for vote in votes:
        is_exist = False
        for select in vote.voteselect_set.all():
            if request.user in select.select_users.all():
                is_exist = True
                break
        vote_exist[vote.title] = is_exist
    print(vote_exist)

    # diary, post, vote list에 담아 최신순 정렬
    writings = list(chain(diaries, posts, votes))
    writings.sort(key=attrgetter('created_at'), reverse=True)

    context = {
        'group': group,
        'notices': notices,
        'vote_form': vote_form,
        'vote_exist': vote_exist,
        'writings': writings,
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


# 멤버 삭제
@login_required
def member_delete(request, group_pk, username):
    group = Group.objects.prefetch_related('group_users').get(pk=group_pk)
    if not group.group_users.filter(pk=request.user.pk).exists():
        return redirect('groups:index')
    
    if request.user != group.chief:
        return redirect('groups:group_detail', group.pk)
    
    member = get_user_model().objects.get(username=username)
    group.group_users.remove(member)
    return redirect('groups:group_setting', group.pk)


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
            return redirect('groups:post_detail', group.pk, post.pk)
    else:
        form = PostForm()
        # post_image_form = PostImageForm()
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
        return redirect('groups:post_detail', group.pk, post.pk)


# 댓글 수정(비동기처리 가정하고 만들었습니다)
@login_required
def comment_update(request, group_pk, post_pk, comment_pk):
    group = Group.objects.get(pk=group_pk)
    if not group.group_users.filter(pk=request.user.pk).exists():
        return redirect('groups:index')
    
    comment = PostComment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        # 여기서 ajax로 데이터 받아서 저장하고 context에 담아 Jsonresponse반환?
        context = {

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

        for option in options:
            VoteSelect.objects.create(vote=vote, content=option)
    # 유효성검사 통과하지 못한 경우(else) 에러메세지 추후 적용
    return redirect('groups:group_detail', group.pk)


# 사용자 투표 행사/취소
@login_required
def throw_vote(request, group_pk, vote_pk, option_pk):
    group = Group.objects.get(pk=group_pk)
    if not group.group_users.filter(pk=request.user.pk).exists():
        return redirect('groups:index')

    vote = Vote.objects.get(pk=vote_pk)
    vote_option = VoteSelect.objects.get(pk=option_pk)
    # 투표 취소
    if vote_option.select_users.filter(pk=request.user.pk).exists():
        vote_option.select_users.remove(request.user)
    # 투표 시행
    else:
        # 중복 투표 가능한 경우 바로 add
        if vote.is_overlap:
            vote_option.select_users.add(request.user)
        else: # 중복 안되는 경우 기존 투표 삭제 후 add
            request.user.selections.clear()
            vote_option.select_users.add(request.user)
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
    # 유효성검사 통과하지 못한 경우(else) 에러메세지 추후 적용
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
    # 유효성검사 통과하지 못한 경우(else) 에러메세지 추후 적용
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