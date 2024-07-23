from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
from .views import DeleteProfilePictureView, DisableUserView, EmployerListView, EnableUserView, IndexView, Profile_detailView, Registration_seekerView, Registration_employerView, S_profile_detailView, SeekerListView, Update_profileView, VerifyEmailView,LoginView,common_page_regView,LogoutDoneView,UpdateJobSeekerProfileView
from .views import ChangePasswordView
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register_seeker', Registration_seekerView.as_view(),name="register_seeker"),
    path('register_employer', Registration_employerView.as_view(),name="register_employer"),
    path('common_page_reg',common_page_regView.as_view(),name="common_page_reg"),#common_page_registration
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('login_user', LoginView.as_view(), name='login_user'),  
    path('logoutdone',LogoutDoneView.as_view(),name="logoutdone"),
    path('update_profile',Update_profileView.as_view(),name="update_profile"),

    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    # path('update_proimg',UploadProfilePictureView.as_view(),name="update_proimg"),
    # path('delete_proimg',RemoveProfilePictureView.as_view(),name="delete_proimg"),

    path('profile_detail',Profile_detailView.as_view(),name="profile_detail"),
    path('update_profile_job',UpdateJobSeekerProfileView.as_view(),name="update_profile_job"),
    path('delete_profile_picture',DeleteProfilePictureView.as_view(),name="delete_profile_picture"),
    path('s_profile_detail',S_profile_detailView.as_view(),name="s_profile_detail"),
    path('Seeker_home',SeekerListView.as_view(),name="Seeker_home"),
    path('emp_home',EmployerListView.as_view(),name="emp_home"),

    path('enable_user/<int:id>/enable/',EnableUserView.as_view(),name="enable_user"),#USER ENABLE FUNCTION
    path('disable_user/<int:id>/disable/',DisableUserView.as_view(),name="disable_user"),#USER DISABLE FUNCTION

   
    path('password_reset',auth_views.PasswordResetView.as_view(),name="password_reset"),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),

   
  


    
]
