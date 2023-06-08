from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, update_session_auth_hash
from .forms import CustomAuthenticationForm, CustomUserCreationForm, CustomUserChangeForm, CustomPasswordChangeForm
from diaries.models import Diary, DiaryShare
from django.core.paginator import Paginator


def login(request):
    if request.user.is_authenticated:
        return redirect('groups:index')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url)
        return redirect('groups:index')
    else:
        form = CustomAuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@login_required
def logout(request):
    auth_logout(request)
        
    return redirect('accounts:login')


def signup(request):
    if request.user.is_authenticated:
        return redirect('groups:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return redirect('groups:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@login_required
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect('accounts:login')


@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', request.user)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('accounts:profile', request.user)
    else:
        form = CustomPasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)


def profile(request, username):
    User = get_user_model()
    person = User.objects.get(username=username)
    diaries = Diary.objects.filter(user=person).order_by('-pk')
    shared_diaries = DiaryShare.objects.filter(diary__user=person).order_by('-pk')
    page= request.GET.get('page', '1')
    per_page = 5

    diaries_paginator = Paginator(diaries, per_page)
    shared_paginator = Paginator(shared_diaries, per_page)

    page_diaries = diaries_paginator.get_page(page)
    page_shared = shared_paginator.get_page(page)
    context = {
        'person': person,
        'diaries': page_diaries,
        'shared_diaries': page_shared,
    }
    return render(request, 'accounts/profile.html', context)