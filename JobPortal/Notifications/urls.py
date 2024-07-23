from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .import views
urlpatterns = [
    # path('chat/', views.chat, name='chat'),
    # path("chat/<str:username>", views.chat, name="chat"),
    # path('messages/<int:sender>/<int:receiver>', views.message_list, name='message_list'),
    # path('messages', views.message_list, name='message_list'),
    # path('search_results_resume_down',views.search_results_resume_down,name="search_results_resume_down"),
    # path('search_results_managejobs',views.search_results_managejobs,name="search_results_managejobs"),
    # path('job_application_list_stat',views.job_application_list_stat,name="job_application_list_stat"),
    # path('', views.Chatview.as_view(), name='chat_room'),
    path('create_chat_room/<int:user_id>/', views.ChatView.as_view(), name='create_chat_room'),
    path('send_message/', views.SendMessageView.as_view(), name='send_message'),
    path('get_messages/', views.GetMessageView.as_view(), name='get_messages'),
    path('user_info/<int:user_id>/', views.UserInfoView.as_view(), name='user_info'),
    path('get_messages/<int:room_id>/', views.GetMessageView.as_view(), name='get_messages'),
    path('load_messages/<int:room_id>/', views.LoadMessagesView.as_view(), name='get_messages'),
]