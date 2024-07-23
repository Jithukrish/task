import random
import string
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import User
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from .forms import RegisterUserForm,ProfileForm,jobseekerProfileForm,CustomPasswordChangeForm
from Resume.models import Resume
from Company.models import Company
from .models import Profile,jobseeker_Profile
from Job.models import JobPost
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView,RedirectView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


  
class IndexView(ListView):
    model = JobPost
    template_name = "index.html"
    context_object_name = 'jobs'

    def get_queryset(self):
        return JobPost.objects.filter(is_active=True).order_by('-timestamp')
def generate_verification_token():
    return get_random_string(length=20)

def send_verification_email(user, request):
    verification_url = request.build_absolute_uri(
        reverse('verify_email', args=[user.verification_token])
    )
    send_mail(
        'Verify your email address',
        f'Please click the link to verify your email: {verification_url}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
class Registration_employerView(View):
    template_name = 'login/register_employer.html'
    form_class = RegisterUserForm
    def get(self, request):
        form = RegisterUserForm()
        return render(request, self.template_name, {'form': form})
    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_employer=True
            user.username=user.email
            user.is_active = False  
            user.verification_token = generate_verification_token()
            user.save()
            Company.objects.create(user=user)
            send_verification_email(user, request)
            messages.info(request,"Successfully created Your Account.Please login")  
            return redirect('login_user')    
        else:
            messages.warning(request,"check your email , password")
            # return redirect('register_employer')
        return render(request, self.template_name, {'form': form})
class Registration_seekerView(View):
    template_name = 'login/register_seeker.html'
    form_class = RegisterUserForm
    def get(self, request):
        form = RegisterUserForm()
        return render(request, self.template_name, {'form': form})
    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_jobseeker=True
            user.username=user.email
            user.is_active = False  
            user.verification_token = generate_verification_token()
            user.save()
            Company.objects.create(user=user)
            send_verification_email(user, request)
            messages.info(request,"Successfully created Your Account.Please login")  
            return redirect('login_user')    
        else:
            messages.warning(request,"check your email , password")
        return render(request, self.template_name, {'form': form})
    
class VerifyEmailView(View):
    def get(self ,request,token):
        try:
            user =User.objects.get(verification_token=token)
            user.is_active =True  
            user.is_verified =True
            user.verification_token = '' 
            user.save()
            messages.success(request, 'Your email has been verified. You can now log in.')
            return redirect('login_user')
        except User.DoesNotExist:
            messages.error(request, 'Invalid verification link')
            return redirect('login_user') 

###########################################################################################################################
# def index(request):
#      jobs=JobPost.objects.filter(is_active=True).order_by('-timestamp')
#      context={
#              'jobs':jobs,
             
#               }
#      return render(request, 'index.html',context)

#--------------------------------------------------------------------------------------------------

# def generate_verification_token():
#     return get_random_string(length=20)

# def send_verification_email(user, request):
#     verification_url = request.build_absolute_uri(
#         reverse('verify_email', args=[user.verification_token])
#     )
#     send_mail(
#         'Verify your email address',
#         f'Please click the link to verify your email: {verification_url}',
#         settings.DEFAULT_FROM_EMAIL,
#         [user.email],
#         fail_silently=False,
#     )

#------------------------------------------------------------------------------------------------------------------
# reg JObseeker
# def register_seeker(request):
#     if request.method == 'POST':
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             user=form.save(commit=False)
#             user.is_jobseeker=True
#             user.username=user.email
#             user.is_active=False 
#             user.verification_token=generate_verification_token()
#             user.save()
#             Resume.objects.create(user=user)   
#             send_verification_email(user, request)
           
#             messages.info(request,"Successfully created Your Account.please login")  
#             return redirect('login_user')    
#         else:
#             messages.warning(request,"Something went wrong")
#             return redirect('register_seeker')
#     else:
#         form = RegisterUserForm()
#         context={'form': form}
#         return render(request,'login/register_seeker.html',context)



# reg  employer
# def register_employer(request):
#     if request.method == 'POST':
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             user=form.save(commit=False)
#             user.is_employer=True
#             user.username=user.email
#             user.is_active = False  
#             user.verification_token = generate_verification_token()

#             user.save()
#             Company.objects.create(user=user)

#             send_verification_email(user, request)
#             messages.info(request,"Successfully created Your Account.Please login")  
#             return redirect('login_user')    
#         else:
#             messages.warning(request,"check your email , password")
#             return redirect('register_employer')
#     else:
#         form = RegisterUserForm()
#         context={'form': form}
#         return render(request,'login/register_employer.html',context)


# def verify_email(request, token):
#     try:
#         user =User.objects.get(verification_token=token)
#         user.is_active =True  
#         user.is_verified =True
#         user.verification_token = '' 
#         user.save()
#         messages.success(request, 'Your email has been verified. You can now log in.')
#         return redirect('login_user')
#     except User.DoesNotExist:
#         messages.error(request, 'Invalid verification link')
#         return redirect('login_user')  

class LoginView(View):
    template_name = 'login/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None and user.is_active:
            login(request, user)
            if request.user.is_jobseeker:
                return redirect('jobseeker_dash')
            elif request.user.is_employer:
                # return redirect('emp_home')
                return redirect('jobseeker_dash')
            else:
                return redirect('login_user')
        else:
            messages.warning(request, 'Check your email and password')
            return redirect('login_user')


# def login_user(request):
#     if request.method =="POST":
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         user=authenticate(request,username=email,password=password)
#         if user is not None and user.is_active:
#             login(request,user)
           
#             if request.user.is_jobseeker:
#                 return redirect('Seeker_home')
#             elif request.user.is_employer:
#                 return redirect('emp_home')
#             else:
#                 return redirect('login_user')
#         else:
#             messages.warning(request, 'Check your email and password')
#             return redirect('login_user')
#     else:
#         return render(request,'login/login.html')

# def common_page_reg(request):
#     return render(request, 'common_reg.html')
class common_page_regView(View):
    def get(self, request):
        return render(request, 'common_reg.html')
    


class LogoutDoneView(View):
    def get(self, request):
        logout(request)     
        messages.info(request, 'Logged out successfully')
        return redirect('login_user')
        
# def logoutdone(request):
#     logout(request)
#     print("logout")
#     messages.info(request, 'Logged out successfully')
#     return redirect('login_user')

 #------------------------------------------------------------------------------------               
#add profile  employer
# def update_profile(request):
#     if not request.user.is_authenticated or not request.user.is_employer:
#         messages.warning(request, 'Permission denied.')
#         return redirect('jobseeker_dash')

    # try:
    #     profile = Profile.objects.get(user=request.user)
    # except Profile.DoesNotExist:
    #     profile = Profile(user=request.user)
    #     # profile=profile.objects.get(user=request.user)
    #     if request.method == 'POST':
    #         form=ProfileForm(request.POST, request.FILES, instance=profile)
    #         if form.is_valid():
    #             var=form.save(commit=False)
    #             user=User.objects.get(id=request.user.id)
    #             user.has_company=True
    #             var.save()
    #             user.save()
    #             messages.info(request, 'Your company is Active. you start create new job')
    #             return redirect('jobseeker_dash')
    #         else:
    #             messages.warning(request, 'something went wrong')
    #     else:
    #         form=ProfileForm(instance=profile)
    #         context={
    #             'form':form
    #         }
    #         return render(request, 'Employer/e_profile.html', context)
    # else:
    #     messages.warning(request,'permission denied')
    #     return redirect('jobseeker_dash')
#------------------------------------------------------------------------------------------------



# class Update_profileView(LoginRequiredMixin, View):
#     login_url = 'login_user'
#     def get(self, request):
#         try:
#             profile=Profile.objects.get(user=request.user)
#         except Profile.DoesNotExist:
#             profile= Profile(user=request.user)
#         form = ProfileForm(instance=profile)
#         context = {
#             'form': form
#         }
#         return render(request, 'Employer/e_profile.html', context)
#     def post(self, request):
#         try:
#             profile = Profile.objects.get(user=request.user)
#         except Profile.DoesNotExist:
#             profile = Profile(user=request.user)

#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             request.user.has_company = True
#             request.user.save()
#             messages.info(request, 'Your profile has been updated successfully.')
#             return redirect('update_profile')
#         else:
#             messages.warning(request, 'Something went wrong. Please check the form.')

#         context = {
#             'form': form
#         }
#         return render(request, 'Employer/e_profile.html', context)

class Update_profileView(LoginRequiredMixin, View):
    login_url = 'login_user'
    def get(self, request):
        try:
            profile=Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile= Profile(user=request.user)
        form = ProfileForm(instance=profile)
        context = {
            'form': form
        }
        return render(request, 'profile/eprofile.html', context)
    def post(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)

        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            request.user.has_company = True
            request.user.save()
            messages.info(request, 'Your profile has been updated successfully.')
            return redirect('update_profile')
        else:
            messages.warning(request, 'Something went wrong. Please check the form.')

        context = {
            'form': form
        }
        return render(request, 'profile/eprofile.html', context)
    

# class UploadProfilePictureView(LoginRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         profile = Profile.objects.get(user=request.user)
#         if 'profile_picture' in request.FILES:
#             profile.profile_picture = request.FILES['profile_picture']
#             profile.save()
#         return redirect(reverse('profile'))  

# class RemoveProfilePictureView(LoginRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         profile = Profile.objects.get(user=request.user)
#         if profile.profile_picture:
#             profile.profile_picture.delete()
#             profile.save()
#         return redirect(reverse('profile')) 
from django.contrib.auth.views import PasswordChangeView as BasePasswordChangeView
from django.urls import reverse_lazy
class ChangePasswordView(BasePasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('password_change_done')  
    template_name = 'profile/eprofile.html'

    def form_valid(self, form):
        messages.success(self.request, 'Your password was successfully updated.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the error below.')
        return super().form_invalid(form)







# def update_profile(request):
#     if not request.user.is_authenticated or not request.user.is_employer:
#         messages.warning(request, 'Permission denied.')
#         return redirect('emp_home')

#     try:
#         profile=Profile.objects.get(user=request.user)
#     except Profile.DoesNotExist:
#         profile= Profile(user=request.user)

#     if request.method == 'POST':
#         form =ProfileForm(request.POST, request.FILES,instance=profile)
#         if form.is_valid():
#             form.save()
#             user =request.user
#             user.has_company =True
#             user.save()
#             messages.info(request, 'Your profile has been updated successfully.')
#             return redirect('update_profile')
#         else:
#             messages.warning(request, 'Something went wrong. Please check the form.')
#     else:
#         form = ProfileForm(instance=profile)

#     context = {
#         'form': form
#     }
#     return render(request, 'Employer/e_profile.html', context)


# def profile_detail(request, id):
#     profile=Profile.objects.get(id=id)
#     context={
#         'profile':profile
#     }
#     return render(request, 'Employer/profile_detail.html', context)
class Profile_detailView(DetailView):
   model=Profile
   template_name='Employer/profile_detail.html'
   context_object_name='profile'
   pk_url_kwarg = 'id'

#########add job seeker  Profile
class Update_profileView(LoginRequiredMixin, View):
    login_url = 'login_user'
    def get(self, request):
        try:
            profile=Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile= Profile(user=request.user)
        form = ProfileForm(instance=profile)
        context = {
            'form': form
        }
        return render(request, 'profile/eprofile.html', context)
    def post(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)

        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            request.user.has_company = True
            request.user.save()
            messages.info(request, 'Your profile has been updated successfully.')
            return redirect('update_profile')
        else:
            messages.warning(request, 'Something went wrong. Please check the form.')

        context = {
            'form': form
        }
        return render(request, 'profile/eprofile.html', context)


class UpdateJobSeekerProfileView(View):
    template_name = "Profile/sprofile.html"
    form_class = jobseekerProfileForm
    def get(self, request):
        if not request.user.is_authenticated or not request.user.is_jobseeker:
            messages.warning(request, 'Permission denied.')
            return redirect('update_profile_job')

        try:
            profile =jobseeker_Profile.objects.get(user=request.user)
        except jobseeker_Profile.DoesNotExist:
            profile =jobseeker_Profile(user=request.user)
        form = self.form_class(instance=profile)
        context = {
            'form': form,
            'profile': profile,
        }
        return render(request, self.template_name, context)
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_jobseeker:
            messages.warning(request, 'Permission denied.')
            return redirect('update_profile_job')
        
        try:
            profile = jobseeker_Profile.objects.get(user=request.user)
        except jobseeker_Profile.DoesNotExist:
            profile = jobseeker_Profile(user=request.user)
        
        form = jobseekerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            var =form.save(commit=False)
            user =User.objects.get(id=request.user.id)
            user.has_resume = True

            var.save()
            form.save_m2m()
            user.save()
            messages.info(request, 'Updated your profile.')
            return redirect('update_profile_job')
        else:
            messages.warning(request, 'Something went wrong. Please check the form for errors.')
        context = {
            'form': form,
            'profile': profile,
        }
        return render(request, 'Profile/sprofile.html', context)
            

class DeleteProfilePictureView(LoginRequiredMixin,View):
    def post(self, request, *args, **kwargs):
        profile=jobseeker_Profile.objects.get(user=request.user)
        if profile.profile_picture:
            profile.profile_picture.delete()
        return redirect('update_profile_job')

 
# def update_profile_job(request):
#     if not request.user.is_authenticated or not request.user.is_jobseeker:
#         messages.warning(request, 'Permission denied.')
#         return redirect('Seeker_home')

#     try:
#         profile =jobseeker_Profile.objects.get(user=request.user)
#     except jobseeker_Profile.DoesNotExist:
#         profile =jobseeker_Profile(user=request.user)

#     if request.method =='POST':
#         form = jobseekerProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             var =form.save(commit=False)
#             user =User.objects.get(id=request.user.id)
#             user.has_resume = True

#             var.save()
#             form.save_m2m()
#             user.save()
#             messages.info(request, 'Updated your profile.')
#             return redirect('Seeker_home')
#         else:
#             messages.warning(request, 'Something went wrong. Please check the form for errors.')
    
#     form = jobseekerProfileForm(instance=profile)
#     context = {
#         'form': form,
#         'profile': profile,
#     }
#     return render(request, 'seeker/s_profile.html', context)


# def s_profile_detail(request, id):
#     profile=jobseeker_Profile.objects.get(id=id)
#     context={
#         'profile':profile
#     }
#     return render(request, 'seeker/s_profile_detail.html', context)

class S_profile_detailView(DetailView):
    model = jobseeker_Profile
    template_name = "seeker/s_profile_detail.html"
    context_object_name='profile'
    pk_url_kwarg = 'id'

   
#admin enable or disable users
class EnableUserView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        user=User.objects.get(id=self.kwargs['id'])
        if not self.request.user.is_superuser:
            return HttpResponse('''<script>alert("Permission denied."); history.go(-1);</script>''')
        if user.is_active:
            return HttpResponse('''<script>alert("User already active."); history.go(-1);</script>''')
        user.is_active = True
        user.save()
        return HttpResponse('''<script>alert("User enabled successfully."); history.go(-1);</script>''')

class DisableUserView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        user=User.objects.get(id=self.kwargs['id'])
        if not self.request.user.is_superuser:
             return HttpResponse('''<script>alert("permission denied");</script>''')
        user=User.objects.get(id=id)
        if not user.is_active:
            return HttpResponse('''<script>alert("User Disable");</script>''')
        user.is_active = False
        user.save()
        return HttpResponse('''<script>alert("User disable Successfully");</script>''')

# 
# def enable_user(request, id):
#     if not request.user.is_superuser:
#     #    return HttpResponse('''<script>alert("login failed");window.location="/"</script>''')
#        return HttpResponse('''<script>alert("permission denied");</script>''')
#     user=User.objects.get(id=id)
#     if user.is_active:

#         return HttpResponse('''<script>alert("User already Active");</script>''')
#     user.is_active = True
#     user.save()
#     return HttpResponse('''<script>alert("User enable Successfully");</script>''')

# def disable_user(request, id):
#     if not request.user.is_superuser:
#        return HttpResponse('''<script>alert("permission denied");</script>''')
#     user=User.objects.get(id=id)
#     if not user.is_active:

#         return HttpResponse('''<script>alert("User Disable");</script>''')
#     user.is_active = False
#     user.save()
#     return HttpResponse('''<script>alert("User disable Successfully");</script>''')

# 
# def Seeker_home(request):
#     companies =Company.objects.all()  
#     context ={
#         'companies': companies,
#     }
#     return render(request, 'dash/shome.html', context)
# class SeekerHomeView(ListView):
#     template_name = 'dash/shome.html'
#     context_object_name = 'companies'
#     queryset = Company.objects.all()
class SeekerListView(ListView):
    template_name='dash/shome.html'
    context_object_name='companies'
    
    def get_queryset(self):
        return Company.objects.all()
class EmployerListView(ListView):
    template_name='dash/ehome.html'
    context_object_name='companies'
    
    def get_queryset(self):
        return Company.objects.filter(user=self.request.user) 
# def emp_home(request):
#     companies =Company.objects.filter(user=request.user) 
#     context ={
#         'companies': companies,
#     }
#     return render(request,'dash/ehome.html',context)
