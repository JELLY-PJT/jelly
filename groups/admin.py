from django.contrib import admin
from .models import Group, Post, PostImage, PostEmote, PostComment, Vote, VoteSelect


admin.site.register(Group)
admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(PostEmote)
admin.site.register(PostComment)
admin.site.register(Vote)
admin.site.register(VoteSelect)