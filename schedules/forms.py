from django import forms
from .models import Schedule, GroupSchedule

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = '__all__'
        exclude = ('user',)


class GroupScheduleForm(forms.ModelForm):
    class Meta:
        model = GroupSchedule
        fields = '__all__'
        exclude = ('group', 'create_user', 'join_users', )