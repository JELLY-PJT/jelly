from rest_framework import serializers
from groups.models import Group
from django.utils.translation import gettext_lazy as _


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'thumbnail']