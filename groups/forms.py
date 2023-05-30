from django import forms
from .models import Group, Post, PostComment, Vote, VoteSelect


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'thumbnail', 'intro',)