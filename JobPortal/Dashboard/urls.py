from django.urls import path
from .import views

urlpatterns = [
    # path('',views.proxy,name="proxy"),
    path('jobseeker_dash',views.JobseekerDashboardView.as_view(),name="jobseeker_dash"),
    path('homepage',views.HomeDashboardView.as_view(),name="homepage"),
    
]
