from django import forms
from .models import Group, Post, PostImage, PostComment, Vote, VoteSelect
from imagekit.forms import ProcessedImageField

class GroupForm(forms.ModelForm):
    name = forms.CharField(label='그룹 이름',  widget=forms.TextInput(
        attrs={'class': 'create-form','style' : 'width:400px;'}))
    thumbnail = ProcessedImageField(
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'create-form','style' : 'width:400px;'}),
        label='그룹프로필 이미지',
        label_suffix='',
        spec_id='image_size',
    )
    intro = forms.CharField(label='그룹 소개', widget=forms.Textarea(
        attrs={'class': 'create-form','style' : 'width:400px;'}))
    class Meta:
        model = Group
        fields = ('name', 'thumbnail', 'intro',)


class PostForm(forms.ModelForm):
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
    class Meta:
        model = PostComment
        fields = ('content',)