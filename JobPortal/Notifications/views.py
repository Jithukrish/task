
from collections import defaultdict
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
from .models import Thread
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


def chat(request):
   threads = Thread.objects.by_user(user=request.user).prefetch_related ('chat_messages').order_by('time_stamp')
   context = {
        'Threads': threads
   }
   return render(request,'Dashboard/chatEmo.html' ,context)

