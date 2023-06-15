from rest_framework import serializers
from groups.models import Group
from django.utils.translation import gettext_lazy as _


class GroupSerializer(serializers.ModelSerializer):
    calendar = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Group
        fields = ['id', 'name', 'calendar', 'thumbnail', ]