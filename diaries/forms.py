from django import forms
from .models import Diary, DiaryComment

class DiaryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].required = False
        # tailwind 클래스 추가
        self.fields["content"].label = ''
        self.fields["title"].widget.attrs['class'] = "block py-2.5 px-1 mb-8 w-full text-2xl text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none focus:outline-none focus:ring-0 focus:border-[var(--color-main-light)] peer"
        self.fields["title"].widget.attrs['placeholder'] = '제목을 입력하세요'
        self.fields["title"].label = ''

        
    class Meta:
        model = Diary
        fields = '__all__'
        exclude = ('user', 'share', 'hit', )


class DiaryCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["comment"].widget.attrs["class"] = "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-[var(--color-main-light)] focus:border-[var(--color-main-light)]"
        self.fields["comment"].widget.attrs["placeholder"] = '댓글을 입력해주세요'
        self.fields["comment"].widget.attrs["rows"] = 1
        self.fields["comment"].label = ''


    class Meta:
        model = DiaryComment
        fields = ('comment',)