from django import forms
from .models import Diary, DiaryComment

class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = '__all__'
        exclude = ('user', 'share', 'hit', )


class DiaryCommentForm(forms.ModelForm):
    class Meta:
        model = DiaryComment
        fields = '__all__'