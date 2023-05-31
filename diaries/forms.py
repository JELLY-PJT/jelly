from django import forms
from .models import Diary, DiaryComment

class DiaryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].required = False
        
    class Meta:
        model = Diary
        fields = '__all__'
        exclude = ('user', 'share', 'hit', )


class DiaryCommentForm(forms.ModelForm):
    class Meta:
        model = DiaryComment
        fields = '__all__'