from django import forms
from .models import Group, Post, PostImage, PostComment, Vote, VoteSelect
from imagekit.forms import ProcessedImageField


class GroupForm(forms.ModelForm):
    name = forms.CharField(label='그룹 이름', widget=forms.TextInput(
        attrs={'class': 'create-form',}))
    thumbnail = ProcessedImageField(
        required=True, widget=forms.ClearableFileInput(attrs={'class': 'create-form',}),
        label='그룹 프로필 이미지',
        label_suffix='',
        spec_id='image_size',
    )
    intro = forms.CharField(label='그룹 소개', widget=forms.Textarea(attrs={'class': 'create-form',}))
    
    class Meta:
        model = Group
        fields = ('name', 'thumbnail', 'intro',)


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # tailwind 클래스 추가
        self.fields["content"].label = ''
        self.fields["content"].widget.attrs['class'] = "block px-6 py-4 w-full text-lg text-gray-900 rounded-md border border-gray-300 focus:ring-[var(--color-main-light)] focus:border-[var(--color-main-light)]"
        self.fields["content"].widget.attrs['rows'] = "15"
        # self.fields["content"].widget.attrs['placeholder'] = '내용을 입력하세요'
        self.fields["title"].widget.attrs['class'] = "block py-2.5 px-1 mb-8 w-full text-2xl text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none focus:outline-none focus:ring-0 focus:border-[var(--color-main-light)] peer"
        self.fields["title"].widget.attrs['placeholder'] = '제목을 입력하세요'
        self.fields["title"].label = ''


    class Meta:
        model = Post
        fields = ('title', 'content',)


class PostImageDeleteForm(forms.ModelForm):
    delete_images = forms.ModelMultipleChoiceField(
        label = '삭제할 이미지 선택',
        queryset=PostImage.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )
    class Meta:
        model = PostImage
        fields = []

    # instance(post)의 이미지 참조
    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)
        if instance:
            self.fields['delete_images'].queryset = instance.postimage_set.all()
    
    # 체크한 이미지가 담긴 cleaned_data['delete_images']에서 이미지 삭제
    def save(self, commit=True):
        for image in self.cleaned_data['delete_images']:
            image.delete()


class PostCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].widget.attrs["class"] = "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-[var(--color-main-light)] focus:border-[var(--color-main-light)]"
        self.fields["content"].widget.attrs["placeholder"] = '댓글을 입력해주세요'
        self.fields["content"].widget.attrs["rows"] = 1
        self.fields["content"].label = ''


    class Meta:
        model = PostComment
        fields = ('content',)


class VoteForm(forms.ModelForm):
    title = forms.CharField(
        label='투표 제목',
        widget=forms.TextInput(
            attrs={
                'class': 'vote-form',
            }
        )
    )
    deadline = forms.DateTimeField(
        label='마감 기한',
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'vote-form',
            }
        ),
    )
    is_overlap = forms.BooleanField(
        label='복수 선택',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'vote-checkform',
            }
        ),
        required=False,
    )
    is_annony = forms.BooleanField(
        label='익명 투표',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'vote-checkform',
            }
        ),
        required=False,
    )
    is_addible = forms.BooleanField(
        label='멤버의 선택지 추가 권한',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'vote-checkform',
            }
        ),
        required=False,
    )
    class Meta:
        model = Vote
        fields = ('title', 'deadline', 'is_overlap', 'is_annony', 'is_addible',)