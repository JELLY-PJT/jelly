from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm, UserChangeForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='사용자 ID',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': '사용자 ID',
            }
        )
    )
    password = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': '비밀번호',
            }
        )
    )


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label='사용자 ID',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': '사용자 ID',
            }
        )
    )
    password1 = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': '비밀번호',
            }
        )
    )
    password2 = forms.CharField(
        label='비밀번호 확인',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': '비밀번호 확인',
            }
        )
    )
    nickname = forms.CharField(
        label='닉네임',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': '닉네임',
            }
        )
    )
    email = forms.CharField(
        label='이메일',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'id': '이메일',
            }
        )
    )
    image = forms.ImageField(
        label='프로필 이미지',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
            },
        ),
        required=False,
    )


    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'nickname', 'email', 'image',)


class CustomUserChangeForm(UserChangeForm):
    nickname = forms.CharField(
        label='닉네임',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id' : '닉네임',
            }
        )
    )
    email = forms.CharField(
        label='이메일',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'id' : '이메일',
            }
        )
    )
    image = forms.ImageField(
        label='프로필 이미지',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
                'id' : '프로필 이미지',
            },
        ),
        required=False,
    )

    password = None
    
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('nickname', 'email','image',)


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='기존 비밀번호',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id' : '기존 비밀번호',
            },
        ),
    )
    new_password1= forms.CharField(
        label='새 비밀번호',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id' : '새 비밀번호',
            },
        ),
    )
    new_password2 = forms.CharField(
        label='새 비밀번호 확인',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id' : '새 비밀번호 확인',
            },
        ),
    )   