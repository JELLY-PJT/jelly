from rest_framework import serializers
from .models import Group, Post, PostImage, PostComment, PostEmote, Vote
from django.contrib.auth import get_user_model


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'
        read_only_fields = ('post',)


class PostEmoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostEmote
        fields = '__all__'


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = '__all__'
        read_only_fields = ('user', 'post', 'like_users',)


# post 조회
class PostReadSerializer(serializers.ModelSerializer):
    postimage_set = PostImageSerializer(many=True)
    postemote_set = PostEmoteSerializer(many=True)
    postcomment_set = PostCommentSerializer(many=True)
    comment_count = serializers.IntegerField(source='postcomment_set.count')

    class Meta:
        model = Post
        fields = '__all__'


# post 생성, 수정, 삭제
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('user', 'group', 'hits', 'emote_users',)


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
