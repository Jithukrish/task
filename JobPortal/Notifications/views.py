
from collections import defaultdict
import json
import os
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib import messages
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
# from .models import JobApplicationNotification, JobPost,Education,Skills_job,Apply_Job, Message
from Company.models import Company
from .models import ChatModel,ChatRoom
from UserApplicant.models import User,jobseeker_Profile
from Resume.models import Resume
# from .forms import EducationForm, JobPostForm, SkillForm,UpdateJobPostForm,ApplyJobForm,SalaryRangeForm, MessageForm
from Resume.forms import ResumeForm
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.http import FileResponse
from django.views.generic import FormView,CreateView
from django.views.generic.edit import UpdateView,DeleteView
from django.views.generic import ListView,DetailView,RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count


from Job.models import Message


# def chat(request):
#    threads = Thread.objects.by_user(user=request.user).prefetch_related ('chat_messages').order_by('time_stamp')
#    context = {
#         'Threads': threads
#    }
#    return render(request,'Dashboard/chatEmo.html' ,context)
class ChatView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_employer:
            users = User.objects.filter(apply_job__job__company__user=request.user).distinct()
        else:
            users = User.objects.filter(applyjob__user=request.user).distinct()
        return render(request, 'Dashboard/ChatView.html', {'users': users})

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id') 
        if not user_id:
            return JsonResponse({'error': 'User ID not provided'}, status=400)
        
        other_user = User.objects.get(id=user_id)
        chat_room, created = ChatRoom.objects.get_or_create(
            user1=request.user,
            user2=other_user,
            defaults={'user1': request.user, 'user2': other_user}
        )
        if not created:
            chat_room = ChatRoom.objects.filter(
                user1=other_user, user2=request.user
            ).first()
        return JsonResponse({'room_id': chat_room.id})


class SendMessageView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        data = json.loads(request.body)
        room_id = data.get('room_id')
        message = data.get('message')
        if not room_id or not message:
            return JsonResponse({'error': 'Check message'}, status=400)
        try:
            room = ChatRoom.objects.get(id=room_id)
        except ChatRoom.DoesNotExist:
            return JsonResponse({'error': 'Chat room does not exist'}, status=404)
        if request.user not in [room.user1, room.user2]:
            return JsonResponse({'error': 'Not allowed'}, status=403)
        ChatModel.objects.create(
            room=room,
            user=request.user,
            message=message
        )
        return JsonResponse({'status': 'Message sent'})

class GetMessageView(LoginRequiredMixin, View):
     def get(self, request, room_id, user_id, *args, **kwargs):
          print(f"Room ID: {room_id}, User ID: {user_id}")  
          try:
               room = ChatRoom.objects.get(id=room_id)
          except ChatRoom.DoesNotExist:
               return JsonResponse({'error': 'Chat room does not exist'}, status=404)
          if request.user not in [room.user1, room.user2]:
               return JsonResponse({'error': 'Not allowed'}, status=403)
          messages = ChatModel.objects.filter(room=room).order_by('timestamp')
          if user_id:
               messages = messages.filter(user_id=user_id) 
          messages_data = [
               {
                    'user': msg.user.username,
                    'message': msg.message,
                    'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'user_id': msg.user.id 
               }
               for msg in messages
          ]
          return JsonResponse({'messages': messages_data})

       

class UserInfoView(View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        if not hasattr(user, 'jobseeker_profile'):
            return JsonResponse({'error': 'Profile information is missing'}, status=500)
        profile_picture = user.jobseeker_profile.profile_picture.url if user.jobseeker_profile.profile_picture else '/path/to/default/user.jobseeker_profile/picture.png'
        chat_rooms = ChatRoom.objects.filter(Q(user1=user) | Q(user2=user))
        message_count = ChatModel.objects.filter(room__in=chat_rooms, user=user).count()
        data = {
            'profile_picture': profile_picture,
            'first_name': user.jobseeker_profile.first_name,
            'last_name': user.jobseeker_profile.last_name,
            'message_count': message_count,
            'room_id': chat_rooms.first().id if chat_rooms.exists() else None,
        }
        return JsonResponse(data)
   
           
class LoadMessagesView(View):
    def get(self, request, user_id):
        messages = ChatModel.objects.filter(
            Q(user_id=user_id) | Q(room__in=ChatRoom.objects.filter(Q(user1=user_id) | Q(user2=user_id)))
        ).order_by('timestamp')
        data = {
            'messages': [{'message': msg.message, 'sender': msg.user.username, 'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')} for msg in messages]
        }
        return JsonResponse(data)




