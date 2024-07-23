from rest_framework import serializers
from Job.models import Message
from UserApplicant.models import User



class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField( slug_field='username', queryset=User.objects.all())
    receiver = serializers.SlugRelatedField( slug_field='username', queryset=User.objects.all())
    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp','unread']