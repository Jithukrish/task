from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .import views
urlpatterns = [
    path('chat/', views.chat, name='chat'),
    # path("chat/<str:username>", views.chat, name="chat"),
    # path('messages/<int:sender>/<int:receiver>', views.message_list, name='message_list'),
    # path('messages', views.message_list, name='message_list'),
    # path('search_results_resume_down',views.search_results_resume_down,name="search_results_resume_down"),
    # path('search_results_managejobs',views.search_results_managejobs,name="search_results_managejobs"),
    # path('job_application_list_stat',views.job_application_list_stat,name="job_application_list_stat"),
  
]