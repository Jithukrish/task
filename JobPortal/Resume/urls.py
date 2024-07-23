from django.urls import path
from .import views

urlpatterns = [
    path('update_resume',views.ResumeUploadView.as_view(),name="update_resume"),
    path('resume_details/<int:id>/',views.ResumeView.as_view(),name="resume_details"),
    
]
