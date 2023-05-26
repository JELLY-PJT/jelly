from rest_framework import serializers
from .models import Group
from django.contrib.auth import get_user_model

class UserGroupListSerializer(serializers.ModelSerializer):
    class GroupThumbnailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Group
            fields = ('name', 'thumbnail',)
            
    user_groups = GroupThumbnailSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'user_groups',)


# class GroupSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Group
#         fields = '__all__'