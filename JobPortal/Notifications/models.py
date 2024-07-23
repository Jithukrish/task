from django.db import models

from UserApplicant.models import User
from django.db.models import Q


class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user =kwargs.get('user')
        lookup = Q(first_person=user) | Q(second_person=user)
        qs =self.get_queryset().filter(lookup).distinct()
        return qs
class Thread(models.Model):
    first_person =models.ForeignKey(User, on_delete=models.CASCADE,null = True, blank =True, related_name="first_person")
    second_person =models.ForeignKey(User, on_delete=models.CASCADE,null = True, blank =True, related_name="second_person")
    updated = models.DateTimeField(auto_now=True)
    time_stamp = models.DateTimeField(auto_now_add=True)
    objects = ThreadManager()
    class Meta:
        unique_together =['first_person','second_person']


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread,on_delete=models.CASCADE, blank=True, null=True, related_name='chat_messages')
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timest_amp = models.DateTimeField(auto_now_add=True)

    

