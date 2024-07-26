from django.urls import path
from .import views

urlpatterns = [
    path('messages/',views.messages,name="messages"),
    path('create_thread/', views.CreateThreadView.as_view(), name='create_thread'),
    # path('resume_details/<int:id>/',views.ResumeView.as_view(),name="resume_details"),
    
]
