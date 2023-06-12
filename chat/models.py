from django.db import models
from django.conf import settings

class Message(models.Model):
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_message")
    group = models.ForeignKey('groups.Group', on_delete=models.CASCADE, related_name="group_message")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    # def last_30_messages(self, group):
    #     return Message.objects.filter(group=group).order_by('created_at')[:30]
    
    # @classmethod
    # async def get_latest_message(cls, user, group):
    #     try:
    #         latest_message = cls.objects.filter(user=user, group=group).order_by('-created_at').first()
    #         return latest_message.created_at if latest_message else None
    #     except cls.DoesNotExist:
    #         return None