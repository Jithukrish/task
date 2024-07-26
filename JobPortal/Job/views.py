
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
from .models import DisableJob, JobApplicationNotification, JobPost,Education, SavedJob,Skills_job,Apply_Job, Message
from Company.models import Company
from UserApplicant.models import User,jobseeker_Profile
from Resume.models import Resume
from .forms import DisableJobForm, EducationForm, JobPostForm, SkillForm,UpdateJobPostForm,ApplyJobForm,SalaryRangeForm, MessageForm
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

class AddEducationView(View):
    def post(self, request, *args, **kwargs):
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save()
            return JsonResponse({'name': education.name})  
        else:
            return JsonResponse({'error': 'Form is not valid'}, status=400)
        
class AddSkillView(View):
    def post(self, request, *args, **kwargs):
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save()
            return JsonResponse({'name': skill.name})  
        else:
            return JsonResponse({'error': 'Form is not valid'}, status=400)
class AddSalaryView(View):    
    def post(self, request, *args, **kwargs):
        form = SalaryRangeForm(request.POST)
        if form.is_valid():
            salary_range = form.save()
            return JsonResponse({'success': 'Salary range added successfully', 'salary_range': salary_range.salary_range})
        else:
            return JsonResponse({'error': 'Form is not valid'}, status=400)

class CreateJobPostView(CreateView):
    template_name = 'Job/Create_job_post.html'
    form_class = JobPostForm
    # success_url = '/manage_jobs/'
    success_url = reverse_lazy('manage_jobs') 

    def form_valid(self, form):
        if not self.request.user.is_authenticated or not self.request.user.is_employer:
            messages.warning(self.request, 'Permission denied.',extra_tags='update_job')
            return redirect('emp_home')
        existing_job = JobPost.objects.filter(
            user=self.request.user,
            title=form.cleaned_data['title'],
            overview=form.cleaned_data['overview'],  
            location=form.cleaned_data['location'],  
            salary=form.cleaned_data['salary'],
        ).exists()
        if existing_job:
            messages.error(self.request, 'You have already added a similar job post.',extra_tags='update_job')
            return redirect('create_job_post')
        job_post = form.save(commit=False)
        job_post.user = self.request.user
        job_post.save()
        messages.success(self.request, 'Job post created successfully.',extra_tags='update_job')
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, 'Please check the form .',extra_tags='update_job')
        return super().form_invalid(form)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


      
          

# def create_job_post(request):
#     if not request.user.is_authenticated or not request.user.is_employer:
#         messages.warning(request, 'Permission denied.')
#         return redirect('emp_home')

#     if request.method == 'POST':
#         form = JobPostForm(request.user, request.POST) 
#         if form.is_valid():
#             job_post = form.save(commit=False)
#             job_post.user = request.user 
#             job_post.save()
#             messages.success(request, 'Job post created successfully.')
#             return redirect('manage_jobs')  
#         else:
#             messages.error(request, 'pls check error.')
#     else:
#         form = JobPostForm(request.user)  

#     context = {
#         'form': form
#     }
#     return render(request, 'job/create_job_post.html', context)

   
            
#----------------------------------------------------------------------------------------------------
# def update_job_post(request, id):
#     if request.user.is_authenticated and request.user.is_employer:
#         try:
#             job_post = JobPost.objects.get(user=request.user, id=id)
#             if job_post.company.user != request.user:  
#                 messages.warning(request, "You don't have permission to update this job .")
#                 return redirect('emp_home')
#         except JobPost.DoesNotExist:
#             messages.warning(request, "Job post does not exist.")
#             return redirect('emp_home')
#         if request.method == 'POST':
#             form = UpdateJobPostForm(request.POST, instance=job_post)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, "Job post updated successfully.")
#                 return redirect('emp_home')
#             else:
#                 messages.error(request, "Error occured pls check")
#         else:
#             form = UpdateJobPostForm(instance=job_post)
        
#         context = {
#             'form': form,
#         }
#         return render(request, 'job/update_job_post.html', context)
#     else:
#         messages.warning(request, "You are not authorized to update job posts.")
#         return redirect('jobseeker_dash')

class UpdateJobView(UpdateView):
    model=JobPost
    form_class = UpdateJobPostForm
    template_name = 'Job/Update_job_post.html'
    success_url = '/emp_home/'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_employer:
            try:
                job_post = JobPost.objects.get(user=request.user, id=id)
                if job_post.company.user != request.user:  
                    messages.warning(request, "You don't have permission to update this job .")
                    return redirect('emp_home')
            except JobPost.DoesNotExist:
                messages.warning(request, "Job post does not exist.")
                return redirect('emp_home')
            return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        messages.success(self.request, "Job post updated successfully.")
        return super().form_valid(form)
    def get_object(self, queryset):
        job_post = JobPost.objects.get(user=self.request.user, id=id)
        if job_post.company.user!= self.request.user:
            messages.warning(self.request,"You don't have permission to update this job post." )
            return redirect('emp_home')
        return job_post

#added jobs view list
# def job_details(request,id):
#     job=JobPost.objects.get(id=id)
#     context={'job':job}
#     return render(request,'job/job_post_details.html',context)

class JobDetailsView(DetailView):
    model=JobPost
    template_name='job/job_post_details.html'
    context_object_name="job"
    pk_url_kwarg = 'id'

class ManageJobsView(LoginRequiredMixin, ListView):
    template_name = 'Job/Manage_jobs.html'
    context_object_name = 'jobs'
    model=JobPost
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_employer:
                return super().dispatch(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized to view this page.")
        else:
            return HttpResponse("You need to login to view this page.")


    def get_queryset(self):
        return JobPost.objects.filter(user=self.request.user)
    
# def manage_search_jobs(request):


class SearchManageView(ListView):
    model = JobPost
    template_name = 'Job/Manage_jobs.html'
    context_object_name = 'jobs'
  

    def get_queryset(self):
        query = self.request.GET.get('search', '')
        location = self.request.GET.get('location', '')
        employer = self.request.user.company  
        queryset = JobPost.objects.filter(company=employer) 
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(location__icontains=query)
            )
        if location:
            queryset = queryset.filter(location__icontains=location)
        return queryset




# def manage_jobs(request):
#     if request.user.is_authenticated and request.user.is_employer:
#         jobs = JobPost.objects.filter(user=request.user)
#         context = {
#             'jobs': jobs
#         }
#         return render(request, 'job/manage_jobs.html', context)
#     else:
#         return HttpResponse("You are not authorized to view this page.")
from django.views.generic import UpdateView
class UpdateJobPostView(UpdateView):
    model = JobPost
    form_class = UpdateJobPostForm
    template_name = 'Job/Update_jo.html'
    success_url = reverse_lazy('manage_jobs')
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_employer:
            messages.warning(request, "You have no permission to update job posts.")
            return redirect('update_jobs')
        try:
            job_post = JobPost.objects.get(user=request.user,pk=self.kwargs['pk'])
          
        except JobPost.DoesNotExist:
            messages.warning(request, "Job post does not exist.")
            return redirect('update_jobs')
        if job_post.company.user != request.user:
            messages.warning(request, "You don't have permission to update this job post.")
            return redirect('update_jobs')

        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        messages.success(self.request, "Job post updated successfully.",extra_tags='job_update')
        return super().form_valid(form)

            

# def update_jobs(request, id):
#     if request.user.is_authenticated and request.user.is_employer:
#         try:
#             job_post = JobPost.objects.get(user=request.user, id=id)
#             if job_post.company.user != request.user: 
#                 messages.warning(request, "You don't have permission to update this job post.")
#                 return redirect('emp_home')
#         except JobPost.DoesNotExist:
#             messages.warning(request, "Job post does not exist.")
#             return redirect('emp_home')
#         if request.method == 'POST':
#             form = UpdateJobPostForm(request.POST, instance=job_post)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, "Job post updated successfully.")
#                 return redirect('manage_jobs')
#             else:
#                 messages.error(request, "Error updating job post. Please check the form.")
#         else:
#             form = UpdateJobPostForm(instance=job_post)        
#         context = {
#             'form': form,
#         }
#         return render(request, 'job/update_jo.html', context)
#     else:
#         messages.warning(request, "You are not authorized to update job posts.")
#         return redirect('emp_home')

       

class DeleteJobView(DeleteView):
    model = JobPost
    template_name = "Job/Delete_job.html"
    success_url = reverse_lazy('manage_jobs')
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_employer:
            messages.warning(request, "You are not authorized to delete job posts.")
            return redirect('emp_home')

        try:
            job_post = JobPost.objects.get(pk=self.kwargs['pk'])
        except JobPost.DoesNotExist:
            messages.error(request, "Job not found.")
            return redirect('manage_jobs')
        if job_post.company.user!= request.user:
            messages.warning(request, "You don't have permission to delete this job post.")
            return redirect('emp_home')
        return super().dispatch(request, *args, **kwargs)
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Job deleted successfully.",extra_tags='delete_job')
        return super().delete(request, *args, **kwargs)
        
            
        
    


# def delete_job(request, id):
#     try:
#         job = JobPost.objects.get(id=id)
#     except JobPost.DoesNotExist:
#         messages.error(request, "Job not found.")
#         return redirect('manage_jobs')

#     if request.method == "POST":
#         job.delete()
#         messages.success(request, "Job deleted successfully.")
#         return redirect('manage_jobs')

#     context = {
#         'job': job
#     }
#     return render(request, 'job/delete_job.html', context)
   

#jobs post viewd seeker

class AllJobSeekerView(ListView):
    model=JobPost
    template_name='job/seeker_view_job.html'
    context_object_name='jobs'
    queryset=JobPost.objects.filter(is_active=True).order_by('-timestamp')
    def get_queryset(self):
        return JobPost.objects.filter(is_active=True).order_by('-timestamp')


# def seeker_view_all_jobs(request):
#     jobs=JobPost.objects.filter(is_active=True).order_by('-timestamp')
#     context={
#             'jobs':jobs,
#              }
#     return render(request,'job/seeker_view_job.html',context)


class SearchAllJobsView(ListView):
    model = JobPost
    template_name = 'Job/seeker_view_job.html'
    context_object_name = 'results'

    def get_queryset(self):
        search_query = self.request.GET.get('search')
        location_query = self.request.GET.get('location')
        queryset = JobPost.objects.all()
        if search_query:
            queryset = queryset.filte(
                Q(title__icontains=search_query) |
                Q(location__icontains=search_query) |
                Q(company__name__icontains=search_query) |
                Q(skills__name__icontains=search_query)
            )
        if location_query:
            queryset = queryset.filter(
                Q(location__icontains=location_query)
            )
        return queryset.distinct()
       
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.template_name = 'Job/Job_post_list.html'
        return context
  


 

#search query of jo
# def search_results(request):
#     search_query = request.GET.get('search')
#     if search_query:
#         results = JobPost.objects.filter(
#             Q(title__icontains=search_query) |
#             Q(location__icontains=search_query) |
#             Q(company__name__icontains=search_query) |
#             Q(skills__name__icontains=search_query)
#         ).distinct()
#     else:
#         results = JobPost.objects.none()
#     context = {
#         'results': results
#     }
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         return render(request, 'job/job_post_list.html', context)
#     else:
#         return render(request, 'job/seeker_view_job.html', context)

# class JobApplicationListStatView(ListView):
#     model = Apply_Job
#     template_name = "Job/job_application_list.html"
#     context_object_name = 'applied_jobs'

    # def get_queryset(self):
    #     search_query = self.request.GET.get('search', '')
    #     current_user = self.request.user
    #     jobs_by_employer = JobPost.objects.filter(user=current_user)
    #     if search_query:
    #         jobs_by_employer = jobs_by_employer.filter(
    #             Q(title__icontains=search_query) |
    #             Q(job_type__icontains=search_query) |
    #             Q(experience__icontains=search_query) |
    #             Q(salary__icontains=search_query) |
    #             Q(company__name__icontains=search_query)
    #         ).distinct()
    #     return Apply_Job.objects.filter(job__in=jobs_by_employer).select_related('job', 'user')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

    # def post(self, request, *args, **kwargs):
    #     job_id = request.POST.get('job_id')
    #     new_status = request.POST.get('status')
    #     job_application =Apply_Job.objects.get(id=job_id)
    #     job_application.status = new_status
    #     job_application.save()
    #     return redirect('job_application_list_stat')

    # def render_to_response(self, context, **response_kwargs):
    #     if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
    #         return render(self.request, 'Job/job_app_status.html', context, **response_kwargs)
    #     else:
    #         return super().render_to_response(context, **response_kwargs)

        
    
# def job_application_list_stat(request):
#     search_query = request.GET.get('search', '')
#     current_user = request.user  
#     if request.method == 'POST':
#         job_id = request.POST.get('job_id')
#         new_status = request.POST.get('status')
#         job_application = Apply_Job.objects.get(id=job_id)
#         job_application.status = new_status
#         job_application.save()
#         return redirect('job_application_list_stat')  
#     jobs_by_employer = JobPost.objects.filter(user=current_user)  
#     if search_query:
#         jobs_by_employer = jobs_by_employer.filter(
#             Q(title__icontains=search_query) |
#             Q(job_type__icontains=search_query) |
#             Q(experience__icontains=search_query) |
#             Q(salary__icontains=search_query) |
#             Q(company__name__icontains=search_query)
#         ).distinct()  
#     applied_jobs = Apply_Job.objects.filter(job__in=jobs_by_employer).select_related('job', 'user')
#     context = {
#         'applied_jobs': applied_jobs,
#     }
    
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         return render(request, 'job/job_app_status.html', context)
#     else:
#         return render(request, 'job/job_application_list.html', context)


# class SearchResultManagejobsView(ListView):
# class SearchResultManagejobsView(View):





class SearchResultManagejobsView(ListView):
    model = JobPost
    template_name = 'Job/Manage_jobs.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        location_query = self.request.GET.get('location', '')
        status_query = self.request.GET.get('status', '')
        jobs = JobPost.objects.filter(user=self.request.user)
        if search_query:
            jobs = jobs.filter(
                Q(title__icontains=search_query) |
                Q(company__name__icontains=search_query) |
                Q(skills__name__icontains=search_query)
            )
        if location_query:
            jobs = jobs.filter(location__icontains=location_query)
        if status_query:
            if status_query == 'active':
                jobs = jobs.filter(is_active=True)
            elif status_query == 'inactive':
                jobs = jobs.filter(is_active=False)

        return jobs.distinct()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['location_query'] = self.request.GET.get('location', '')
        context['status_query'] = self.request.GET.get('status', '')
        return context
    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string('Job/Manage_search.html', context, request=self.request)
            return JsonResponse({'html': html})
        return super().render_to_response(context, **response_kwargs)

      
   
   

  
  
       


   
# def search_results_managejobs(request):
#     search_query = request.GET.get('search')
#     location_query = request.GET.get('location')
#     status_query = request.GET.get('status')  
#     jobs = JobPost.objects.all()
#     if search_query:
#         jobs = jobs.filter(
#             Q(title__icontains=search_query) |
#             Q(company__name__icontains=search_query) |
#             Q(skills__name__icontains=search_query)
#         )
#     if location_query:
#         jobs = jobs.filter(location__icontains=location_query)
  
#     if status_query is not None:
#         if status_query == 'active':
#             jobs = jobs.filter(is_active=True)
#         elif status_query == 'inactive':
#             jobs = jobs.filter(is_active=False)
#     context = {
#         'jobs': jobs,
#         'search_query': search_query,
#         'location_query': location_query,       
#         'status_query': status_query,
#     }

#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         return render(request, 'job/manage_search.html', context)
#     else:
#         return render(request, 'job/manage_jobs.html', context)

    

##############################################################################################################


class SearchResultApplicationView(View):
    model = JobPost
    template_name = 'job/user_view_status.html'
    context_object_name ='results'
    def get(self, request):
        search_query = request.GET.get('search')
        current_user = request.user
    
        if search_query:
            applied_jobs = JobPost.objects.filter(
                Q(apply_job__user=current_user),
                Q(title__icontains=search_query) |
                Q(location__icontains=search_query) |
                Q(company__name__icontains=search_query) |
                Q(skills__name__icontains=search_query)
            ).distinct().prefetch_related('apply_job_set', 'company')
        else:
            applied_jobs = JobPost.objects.filter(apply_job__user=current_user).distinct().prefetch_related('apply_job_set', 'company')

        context = {
            'results': applied_jobs,
        }
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, 'job/apppli_post_list.html', context)
        else:
            return render(request, 'job/user_view_status.html', context)

# def search_results_applica(request):
#     search_query = request.GET.get('search')
#     current_user = request.user
    
#     if search_query:
#         applied_jobs = JobPost.objects.filter(
#             Q(apply_job__user=current_user),
#             Q(title__icontains=search_query) |
#             Q(location__icontains=search_query) |
#             Q(company__name__icontains=search_query) |
#             Q(skills__name__icontains=search_query)
#         ).distinct().prefetch_related('apply_job_set', 'company')
#     else:
#         applied_jobs = JobPost.objects.filter(apply_job__user=current_user).distinct().prefetch_related('apply_job_set', 'company')

#     context = {
#         'results': applied_jobs,
#     }

#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         return render(request, 'job/apppli_post_list.html', context)
#     else:
#         return render(request, 'job/user_view_status.html', context)

    
         
#view more selected job

class SeekViewMoreView(DetailView):
    model = JobPost
    template_name = 'Job/seeker_more_jobdetails.html'
    context_object_name = 'jobs'
    pk_url_kwarg = 'id'

# def seeker_viewmore(request,id):
#     jobs=JobPost.objects.get(id=id)
#     context={'jobs':jobs}
#     return render(request,'job/seeker_more_jobdetails.html',context)






#apply user  JOB list

class AppliedJobView(ListView):
    model=Apply_Job
    template_name = 'job/Applied_job_list.html'
    context_object_name = 'applied_jobs'
    paginate_by = 10
    def get_queryset(self):
        return Apply_Job.objects.filter(user=self.request.user).select_related('job')

class SearchAppliedJobs(View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        location_query = request.GET.get('location', '')
        applied_jobs = Apply_Job.objects.filter(
            job__title__icontains=search_query,
            job__location__icontains=location_query,
            user=request.user
        )
        html = render_to_string('Job/applied_jobs_results.html', {'applied_jobs': applied_jobs})
        return JsonResponse({'html': html})

# def applied_job(request):
#     applied_jobs = Apply_Job.objects.filter(user=request.user).select_related('job')
#     context={
#         'applied_jobs':applied_jobs,
#     }
#     return render(request,'job/Applied_jo.html',context)




# class JobApplyView(DetailView):
#     model = JobPost
#     template_name = 'job/apply_job1.html'
#     context_object_name = 'job'
#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object() 
#         has_apply = Apply_Job.objects.filter(user=request.user, job=self.object).exists()
#         context = {'job': self.object, 'has_apply': has_apply}
#         return render(request, self.template_name, context)

    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()  
    #     has_apply = Apply_Job.objects.filter(user=request.user, job=self.object).exists()
    #     if not has_apply and request.method == 'POST':
    #         Apply_Job.objects.create(user=request.user, job=self.object)
    #         return redirect('seeker_view_all_jobs')  
    #     context = {'job': self.object, 'has_apply': has_apply}
    #     return render(request, self.template_name, context)
   
class JobApplyView(DetailView):
    model = JobPost
    template_name = 'Job/Apply_job.html'
    context_object_name = 'job'

    def get_object(self, queryset=None):
        return JobPost.objects.get(id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.object
        has_apply = Apply_Job.objects.filter(user=self.request.user, job=job).exists()
        context['has_apply'] = has_apply
        return context

    def post(self, request, *args, **kwargs):
        job = self.get_object()
        has_apply = Apply_Job.objects.filter(user=request.user, job=job).exists()

        if not has_apply and request.method == 'POST':
            Apply_Job.objects.create(user=request.user, job=job)
          
            messages.success(request, 'You application successfully submitted',extra_tags='apply')
            return redirect('seeker_view_all_jobs')

        context = self.get_context_data()
        return render(request, self.template_name, context)

# def jobPapplyseeker(request, id):
#     job=JobPost.objects.get(id=id)

#     has_apply = Apply_Job.objects.filter(user=request.user, job=job).exists()

#     if request.method == 'POST':
#         if not has_apply:  
#             Apply_Job.objects.create(user=request.user, job=job)
#             return redirect('seeker_view_all_jobs') 

#     has_apply = Apply_Job.objects.filter(user=request.user, job=job).exists()

#     context = {
#         'job': job,
#         'has_apply': has_apply 
#     }
#     return render(request, 'job/apply_job1.html', context)


# class JobApplicationView(FormView):
#     model = JobPost
#     template_name = 'job/apply_job.html'
#     form_class = ApplyJobForm
#     success_url = '/seeker_view_all_jobs/'  

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs

#     def get_initial(self):
#         return super().get_initial()

#     def get(self, request, *args, **kwargs):
#         self.job_post = JobPost.objects.get(pk=self.kwargs['id'])  
#         resume_exists = Resume.objects.filter(user=request.user).exists()
#         if not resume_exists:
#             messages.error(request, 'You cannot apply to a job without uploading a resume.')
#             return redirect('update_resume')
#         return super().get(request, *args, **kwargs)

#     def form_valid(self, form):
#         job = self.job_post  
#         apply_job = form.save(commit=False)
#         apply_job.user = self.request.user
#         apply_job.job = job
#         apply_job.save()
#         messages.success(self.request, 'Job applied successfully!')
#         return super().form_valid(form)

#     def form_invalid(self, form):
#         return self.render_to_response(self.get_context_data(form=form))class JobDetailView(DetailView):
   
class JobApplicationView(DetailView, FormView):
    model = JobPost
    template_name = 'job/apply_job.html'
    context_object_name = 'job'
    form_class = ApplyJobForm

    def get_object(self, queryset=None):
        return JobPost.objects.get(id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['resume'] = Resume.objects.get(user=self.request.user)
        except Resume.DoesNotExist:
            messages.error(self.request, 'You cannot apply to a job without uploading a resume.')
            return redirect('update_resume')  
        return context
    def form_valid(self, form):
        job = self.get_object()
        apply_job = form.save(commit=False)
        apply_job.user = self.request.user
        apply_job.job = job
        apply_job.save()
    
        messages.success(self.request, 'Job applied successfully!')
        return redirect('seeker_view_all_jobs')
    def form_invalid(self, form):
        messages.error(self.request, 'Failed to apply for the job. Please check the form.')
        return super().form_invalid(form)
    def get_success_url(self):
        return redirect('seeker_view_all_jobs')  
   
           


# def job_application(request, id):
#     job = JobPost.objects.get(id=id)
    
#     try:
#         resume = Resume.objects.get(user=request.user)
#     except Resume.DoesNotExist:
#         messages.error(request, 'You cannot apply  job without uploading  resume.')
#         return redirect('update_resume')  

#     if request.method == 'POST':
#         form = ApplyJobForm(request.POST)
#         if form.is_valid():
#             apply_job = form.save(commit=False)
#             apply_job.user = request.user
#             apply_job.job = job
#             apply_job.save()
            
#             messages.success(request, 'Job applied successfully!')
#             return redirect('seeker_view_all_jobs')  
#     else:
#         form = ApplyJobForm()

#     context = {
#         'job': job,
#         'form': form,
#     }
#     return render(request, 'job/apply_job.html', context)

class StatusTarckSeekerView(ListView):
    model = Apply_Job
    template_name = 'Job/user_view_status.html'
    context_object_name = 'jobs'
    def get_queryset(self):
        return Apply_Job.objects.filter(user = self.request.user)

# class StatusTarckSeekerView(ListView):
#     model = Apply_Job
#     template_name = 'job/user_view_status.html'
#     context_object_name = 'jobs'

#     def get_queryset(self):
#         return Apply_Job.objects.filter(user=self.request.user)    

# def status_track_seeker(request):
#     jobs=Apply_Job.objects.filter(user = request.user)
#     context={'jobs':jobs}
#     return render(request,'job/user_view_status.html',context)
class JobApplicationListView(ListView):
    model=Apply_Job
    template_name = 'job/job_application_list_all.html'
    context_object_name = 'job_applications'
    def get_queryset(self, request):
        if request.user.is_authenticated and request.user.is_employer:
           return Apply_Job.objects.filter(job__user=request.user)
        else:
            return Apply_Job.objects.none()
    def render_to_response(self, context, **response_kwargs):
        if self.request.user.is_authenticated and self.request.user.is_employer:
            return HttpResponse("You have no per,miossion to access data.")
        return super().render_to_response(context, **response_kwargs) 
            




# def job_application_list_stats(request):
#     if request.user.is_authenticated and request.user.is_employer:
#         job_applications = Apply_Job.objects.filter(job__user=request.user)
#         context = {
#             'job_applications': job_applications
#         }
#         return render(request, 'job/job_application_list_all.html', context)
#     else:
#         return HttpResponse("only for employer.")

class StatusTrackUpdateEmpView(UpdateView):
    model=Apply_Job
    template_name='Job/update_status.html'
    fields = ['status']
    success_url = '/job_application_list_stats/'
    context_object_name='job'

    def form_valid(self,form):
        # job = Apply_Job.objects.get(id=id)
        job=form.save(commit=False)
        new_status = self.request.POST.get('status')
        job.status = new_status  
        job.save()
        recipient_email = job.user.email
        recipient_name =  job.user.jobseeker_profile.first_name   

        subject = ' Your Job Application Status Update'
        html_message = render_to_string('Job/status_update_email.html', {'recipient_name': recipient_name, 'status': new_status})
        plain_message = strip_tags(html_message)

        send_mail(subject, plain_message, 'your_email@example.com', [recipient_email], html_message=html_message)
        return redirect('job_application_list_stats') 
    def get_success_url(self):
        return reverse_lazy('job_application_list_stats')  
        


    
# def status_track_update_emp(request,id):
#     if request.method == 'POST':
#         job = Apply_Job.objects.get(id=id)
#         new_status = request.POST.get('status')
#         job.status = new_status  
#         job.save()
#         recipient_email = job.user.email
#         recipient_name =  job.user.jobseeker_profile.first_name   

#         subject = ' Your Job Application Status Update'
#         html_message = render_to_string('job/status_update_email.html', {'recipient_name': recipient_name, 'status': new_status})
#         plain_message = strip_tags(html_message)

#         send_mail(subject, plain_message, 'your_email@example.com', [recipient_email], html_message=html_message)
#         return redirect('job_application_list_stats')  
#     else:
#         job = Apply_Job.objects.get(id=id)
#         return render(request, 'job/update_status.html', {'job': job})

#all applications views employer jobs 
class AllApplicationsView(DetailView):
    model = JobPost
    template_name = 'Job/all_applications.html'
    context_object_name = 'job'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.get_object()
        applications = Apply_Job.objects.filter(job=job).select_related('user__resume')

        for application in applications:
            print(application.user.get_full_name())
            print(application.user.username)
            print(application.job.title)

        context['applications'] = applications
        return context
    
    
# def all_applications(request,id):
#     job=JobPost.objects.get(id=id)
#     applications=Apply_Job.objects.filter(job=job).select_related('user__resume')
#     for application in applications:
#         print(application.user.get_full_name())
#         print(application.user.username)
#         print(application.job.title)
#     context = {
#         'job': job,
#         'applications': applications,
#     }
#     return render(request,'job/all_applications.html',context)
    

    
class DownloadResumeView(View):
    def get(self, request, file):
        try:
            resume = Resume.objects.get(id=file)
        except Resume.DoesNotExist:
            raise Http404("Resume not found")
        
        resume_path = resume.resume.path
        if not os.path.exists(resume_path):
            raise Http404("Resume not found")
        
        return FileResponse(open(resume_path, 'rb'), as_attachment=True)

# def download_resume(request, file):
#     resume = Resume.objects.get( id=file)
#     resume_path = resume.resume.path   
#     try:
#         return FileResponse(open(resume_path, 'rb'), as_attachment=True)
#     except FileNotFoundError:
#         raise Http404("Resume not found")
    
    
#view more selected job
class SearchResultsResumeDownloadView(View):
    def get(self, request):
        search_query = request.GET.get('search')
        applications = Apply_Job.objects.none()

        if search_query:
            job_results = JobPost.objects.filter(
                Q(title__icontains=search_query) |
                Q(location__icontains=search_query)
            ).distinct()

            applications = Apply_Job.objects.filter(
                Q(job__in=job_results) |
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query) |
                Q(status__icontains=search_query)
            ).select_related('user', 'job').distinct()

        context = {
            'applications': applications  
        }

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, 'job/check_list.html', context)
        else:
            return render(request, 'job/all_applications.html', context)

# def search_results_resume_down(request):
#     search_query = request.GET.get('search')
#     if search_query:
#        job_results = JobPost.objects.filter(
#             Q(title__icontains=search_query) |
#             Q(location__icontains=search_query)
#         ).distinct()
#        applications = Apply_Job.objects.filter(
#             Q(job__in=job_results) |
#             Q(user__first_name__icontains=search_query) |
#             Q(user__last_name__icontains=search_query) |
#             Q(status__icontains=search_query)
#         ).select_related('user', 'job').distinct()
#     else:
#         applications = Apply_Job.objects.none()
#     context = {
#         'applications': applications  
#     }
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         return render(request, 'job/check_list.html', context)
#     else:
#         return render(request, 'job/all_applications.html', context)

# class SearchStatusListview(ListView):
 


# class SearchStatusListview(ListView):
#     model = Apply_Job
#     template_name = "Job/job_application_list_all.html"
#     context_object_name = 'jobs'

#     def get_queryset(self):
#         search_query = self.request.GET.get('search', '')
#         location_query = self.request.GET.get('location', '')

#         jobs = Apply_Job.objects.filter(user=self.request.user)

#         if search_query:
#             jobs = jobs.filter(
#                 Q(job__title__icontains=search_query)
#             )

#         if location_query:
#             jobs = jobs.filter(
#                 Q(job__location__icontains=location_query)
#             )

#         return jobs.distinct()

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['search_query'] = self.request.GET.get('search', '')
#         context['location_query'] = self.request.GET.get('location', '')
#         return context

#     def render_to_response(self, context, **response_kwargs):
#         if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
#             html = render_to_string('Job/search_status.html', context, request=self.request)
#             return JsonResponse({'html': html})
#         return super().render_to_response(context, **response_kwargs)




class SearchStatusListview(ListView):
    model = Apply_Job
    template_name = "Job/Job_application_list_all.html"
    context_object_name = 'jobs'

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        location_query = self.request.GET.get('location', '')

        jobs = Apply_Job.objects.filter(user=self.request.user)  
        print(jobs)

        if search_query:
            jobs = jobs.filter(
                Q(job__title__icontains=search_query)
            )
        if location_query:
            jobs = jobs.filter(
                Q(job__location__icontains=location_query)
            )

        return jobs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['location_query'] = self.request.GET.get('location', '')
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string('Job/search_status.html', context, request=self.request)
            return JsonResponse({'html': html})
        return super().render_to_response(context, **response_kwargs)


class JobApplicationListStatView(ListView):
    model=Apply_Job     
    template_name = 'Job/Job_application_list_all.html'
    context_object_name="job_applications"
    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_employer:
            return Apply_Job.objects.filter(job__user=self.request.user)
        else:
            return Apply_Job.objects.none()
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_employer:
            return HttpResponse("only for employer.")
        return super().dispatch(request, *args, **kwargs)

# def job_application_list_stats(request):
#     if request.user.is_authenticated and request.user.is_employer:
#         job_applications = Apply_Job.objects.filter(job__user=request.user)
#         context = {
#             'job_applications': job_applications
#         }
#         return render(request, 'job/job_application_list_all.html', context)
#     else:
#         return HttpResponse("only for employer.")




# -----------------------------------report section--------------------------------
from django.utils.timezone import now
from datetime import date

        
class JobApplicationCountView(ListView):
    model = JobPost
    template_name = 'Dashboard/Dashboard.html'
    context_object_name = 'applications'

    def get_queryset(self):
        filter_option = self.request.GET.get('filter', 'month')
        queryset = super().get_queryset()

        if filter_option == 'today':
            start_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=1)
            queryset = queryset.filter(timestamp__range=(start_date, end_date))
        elif filter_option == 'week':
            start_date = timezone.now() - timedelta(days=timezone.now().weekday())
            queryset = queryset.filter(timestamp__gte=start_date)
        elif filter_option == 'month':
            start_date = timezone.now().replace(day=1)
            queryset = queryset.filter(timestamp__gte=start_date)
        elif filter_option == 'year':
            start_date = timezone.now().replace(month=1, day=1)
            queryset = queryset.filter(timestamp__gte=start_date)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_applications'] = self.get_queryset().count()
        return context
#-----------------------------------employer --------------------------------------------------------
class JobPostCountView(LoginRequiredMixin, ListView):
    model = JobPost
    template_name = 'Dashboard/Dashboard.html'
    context_object_name = 'job_posts'

    def get_queryset(self):
        filter_option = self.request.GET.get('filter', 'all')
        queryset = super().get_queryset().filter(user=self.request.user)  

        if filter_option == 'today':
            start_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=1)
            queryset = queryset.filter(timestamp__range=(start_date, end_date))
        elif filter_option == 'week':
            start_date = timezone.now() - timedelta(days=timezone.now().weekday())
            queryset = queryset.filter(timestamp__gte=start_date)
        elif filter_option == 'month':
            start_date = timezone.now().replace(day=1)
            queryset = queryset.filter(timestamp__gte=start_date)
        elif filter_option == 'year':
            start_date = timezone.now().replace(month=1, day=1)
            queryset = queryset.filter(timestamp__gte=start_date)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_job_posts'] = self.get_queryset().count()
        return context




class JobPostCountRecivedView(LoginRequiredMixin, ListView):
    model = JobPost
    template_name = 'Dashboard/Dashboard.html'
    context_object_name = 'job_posts'

    def get_queryset(self):
        filter_option = self.request.GET.get('filter', 'all')
        user = self.request.user
        queryset = JobPost.objects.filter(user=user) 

        if filter_option == 'today':
            start_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=1)
            queryset = queryset.filter(timestamp__range=(start_date, end_date))
        elif filter_option == 'week':
            start_date = timezone.now() - timedelta(days=timezone.now().weekday())
            queryset = queryset.filter(timestamp__gte=start_date)
        elif filter_option == 'month':
            start_date = timezone.now().replace(day=1)
            queryset = queryset.filter(timestamp__gte=start_date)
        elif filter_option == 'year':
            start_date = timezone.now().replace(month=1, day=1)
            queryset = queryset.filter(timestamp__gte=start_date)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_posts = self.get_queryset()
        applied_users_count = 0
        for job_post in job_posts:
            applied_users_count += Apply_Job.objects.filter(job=job_post).count()
        context['applied_users_count'] = applied_users_count
        return context

class AcceptedApplicationsCountView(LoginRequiredMixin, ListView):
    model = JobPost
    template_name = 'Dashboard/Dashboard.html'
    context_object_name = 'job_posts'

    def get_queryset(self):
        filter_option = self.request.GET.get('filter', 'all')
        user = self.request.user
        queryset = JobPost.objects.filter(user=user) 

        if filter_option == 'today':
            start_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=1)
            queryset = queryset.filter(timestamp__range=(start_date, end_date))
        elif filter_option == 'week':
            start_date = timezone.now() - timedelta(days=timezone.now().weekday())
            queryset = queryset.filter(timestamp__gte=start_date)
        elif filter_option == 'month':
            start_date = timezone.now().replace(day=1)
            queryset = queryset.filter(timestamp__gte=start_date)
        elif filter_option == 'year':
            start_date = timezone.now().replace(month=1, day=1)
            queryset = queryset.filter(timestamp__gte=start_date)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_posts = self.get_queryset()
        accepted_applications_count = 0

        for job_post in job_posts:
            accepted_applications_count += Apply_Job.objects.filter(job=job_post, status='Accepted').count()

        context['accepted_applications_count'] = accepted_applications_count
        return context


class RejectedApplicationsCountView(LoginRequiredMixin, ListView):
    model = JobPost
    template_name = 'Dashboard/Dashboard.html'
    context_object_name = 'job_posts'

    def get_queryset(self):
        filter_option = self.request.GET.get('filter', 'all')
        user = self.request.user
        queryset = JobPost.objects.filter(user=user) 

        if filter_option == 'today':
            start_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=1)
            queryset = queryset.filter(timestamp__range=(start_date, end_date))
        elif filter_option == 'week':
            start_date = timezone.now() - timedelta(days=timezone.now().weekday())
            queryset = queryset.filter(timestamp__gte=start_date)
        elif filter_option == 'month':
            start_date = timezone.now().replace(day=1)
            queryset = queryset.filter(timestamp__gte=start_date)
        elif filter_option == 'year':
            start_date = timezone.now().replace(month=1, day=1)
            queryset = queryset.filter(timestamp__gte=start_date)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_posts = self.get_queryset()
        accepted_applications_count = 0
        for job_post in job_posts:
            accepted_applications_count += Apply_Job.objects.filter(job=job_post, status='Rejected').count()
        context['rejected_applications_count'] = accepted_applications_count
        return context

    
class PendingApplicationsCountView(LoginRequiredMixin, ListView):
    model = JobPost
    template_name = 'Dashboard/Dashboard.html'
    context_object_name = 'job_posts'

    def get_queryset(self):
        filter_option = self.request.GET.get('filter', 'all')
        user = self.request.user
        queryset = JobPost.objects.filter(user=user) 

        if filter_option == 'today':
            start_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=1)
            queryset = queryset.filter(timestamp__range=(start_date, end_date))
        elif filter_option == 'week':
            start_date = timezone.now() - timedelta(days=timezone.now().weekday())
            queryset = queryset.filter(timestamp__gte=start_date)
        elif filter_option == 'month':
            start_date = timezone.now().replace(day=1)
            queryset = queryset.filter(timestamp__gte=start_date)
        elif filter_option == 'year':
            start_date = timezone.now().replace(month=1, day=1)
            queryset = queryset.filter(timestamp__gte=start_date)
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_posts = self.get_queryset()
        accepted_applications_count = 0
        for job_post in job_posts:
            accepted_applications_count += Apply_Job.objects.filter(job=job_post, status='Pending').count()
        context['pending_applications_count'] = accepted_applications_count
        return context
    
          






# class ReportsstatusView(TemplateView):
#     template_name = 'Dashboard/Dashboard.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         today = datetime.now().date()
#         start_date_week = today - timedelta(days=today.weekday())  
#         start_date_month = today.replace(day=1)
#         start_date_year = today.replace(month=1, day=1)

#         job_posts = JobPost.objects.filter(user=self.request.user)

#         counts_today = Apply_Job.objects.filter(job__in=job_posts, timestamp__date=today).values('status').annotate(count=Count('id'))
#         counts_week = Apply_Job.objects.filter(job__in=job_posts, timestamp__date__gte=start_date_week).values('status').annotate(count=Count('id'))
        # counts_month = Apply_Job.objects.filter(job__in=job_posts, timestamp__date__gte=start_date_month).values('status').annotate(count=Count('id'))
        # counts_year = Apply_Job.objects.filter(job__in=job_posts, timestamp__date__gte=start_date_year).values('status').annotate(count=Count('id'))

        # applied_users_today = Apply_Job.objects.filter(job__in=job_posts, timestamp__date=today).select_related('user')
        # applied_users_week = Apply_Job.objects.filter(job__in=job_posts, timestamp__date__gte=start_date_week).select_related('user')
        # applied_users_month = Apply_Job.objects.filter(job__in=job_posts, timestamp__date__gte=start_date_month).select_related('user')
        # applied_users_year = Apply_Job.objects.filter(job__in=job_posts, timestamp__date__gte=start_date_year).select_related('user')

        # context['counts_today'] = counts_today
        # context['counts_week'] = counts_week
        # context['counts_month'] = counts_month
        # context['counts_year'] = counts_year

        # context['applied_users_today'] = applied_users_today
        # context['applied_users_week'] = applied_users_week
        # context['applied_users_month'] = applied_users_month
        # context['applied_users_year'] = applied_users_year

        # return context

    # def post(self, request, *args, **kwargs):
    #     if 'update_status' in request.POST:
    #         job_post_id = request.POST.get('job_post_id')
    #         apply_job_id = request.POST.get('apply_job_id')
    #         new_status = request.POST.get('new_status')

        #     try:
        #         apply_job = Apply_Job.objects.get(id=apply_job_id)
        #         apply_job.status = new_status
        #         apply_job.save()
        #     except Apply_Job.DoesNotExist:
        #         pass

        #     return redirect(reverse('jobseeker_dash'))

        # return super().get(request, *args, **kwargs)

# class ReportsstatusView(TemplateView):
#     template_name = 'Dashboard/Dashboard.html'
# class ReportsstatusView(TemplateView):




class ReportsstatusView(TemplateView):
    template_name = 'Dashboard/Dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        start_date_week = today - timedelta(days=today.weekday())
        start_date_month = today.replace(day=1)
        start_date_year = today.replace(month=1, day=1)

        filter_param = self.request.GET.get('filter', 'today')

        if filter_param == 'month':
            start_date = start_date_month
            context['filter_title'] = "This Month"
        elif filter_param == 'year':
            start_date = start_date_year
            context['filter_title'] = "This Year"
        else:
            start_date = today
            context['filter_title'] = "Today"

        job_posts = JobPost.objects.filter(user=self.request.user)
        print(f"Filter: {filter_param}, Start Date: {start_date}")
        print(f"Job Posts: {job_posts}")
        counts = Apply_Job.objects.filter(
            job__in=job_posts,
            status__in=['Pending', 'Accepted', 'Rejected'],
            timestamp__date__gte=start_date
        ).values('status').annotate(count=Count('id'))

        print(f"Counts: {counts}")

        context['counts'] = counts

        return context


    

       

    
          
          
              

   
class RecentAppliedJobsListView(ListView):
    model = Apply_Job  
    template_name = 'Dashboard/Dashboard.html'
    context_object_name = 'recent_applied_jobs'

    def get_queryset(self):
        filter_option = self.request.GET.get('filter', 'today')
        queryset = Apply_Job.objects.all()

        if filter_option == 'today':
            queryset = queryset.filter(timestamp__date=date.today())
            filter_option_text = 'Today'
        elif filter_option == 'this_month':
            queryset = queryset.filter(timestamp__month=date.today().month)
            filter_option_text = 'This Month'
        elif filter_option == 'this_year':
            queryset = queryset.filter(timestamp__year=date.today().year)
            filter_option_text = 'This Year'
        else:
            filter_option_text = 'All'  
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_option = self.request.GET.get('filter', 'today')
        if filter_option == 'today':
            filter_option_text = 'Today'
        elif filter_option == 'this_month':
            filter_option_text = 'This Month'
        elif filter_option == 'this_year':
            filter_option_text = 'This Year'
        else:
            filter_option_text = 'All'  
        context['filter_option'] = filter_option_text
        return context

class AppliedJobSeekersListView(LoginRequiredMixin, ListView):
    template_name = 'dashboard/applied_job_seekers.html'
    context_object_name = 'applied_job_seekers'
    paginate_by = 10  
    def get_queryset(self):
        employer_company = self.request.user.company  
        applied_job_seekers = Apply_Job.objects.filter(
            job__employer=employer_company
        ).select_related('user').order_by('-timestamp')
        return applied_job_seekers
 

    
     


#-----------------------------------employer --------------------------------------------------------

#-----------------------------------employer --------------------------------------------------------
#-----------------------------------employer --------------------------------------------------------
#-----------------------------------employer --------------------------------------------------------
#-----------------------------------employer --------------------------------------------------------
#-----------------------------------employer --------------------------------------------------------
class JobAppliListview(ListView):
    model = Apply_Job
    template_name = 'Dashboard/Dashboard.html'
    context_object_name = 'applied_jobs'  
    def get_queryset(self):
        filter_option = self.request.GET.get('filter', 'month')
        queryset = Apply_Job.objects.all()  
        if filter_option == 'today':
            start_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=1)
            queryset = queryset.filter(timestamp__range=(start_date, end_date))
        elif filter_option == 'week':
            start_date = timezone.now() - timedelta(days=timezone.now().weekday())
            queryset = queryset.filter(timestamp__gte=start_date)
        elif filter_option == 'month':
            start_date = timezone.now().replace(day=1)
            queryset = queryset.filter(timestamp__gte=start_date)
        elif filter_option == 'year':
            start_date = timezone.now().replace(month=1, day=1)
            queryset = queryset.filter(timestamp__gte=start_date)

        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_applied_jobs'] = self.get_queryset().count()
        print('Total applied jobs:', context['total_applied_jobs'])  
        return context

class AcceptedApplicationsView(ListView):
    model = Apply_Job
    template_name = 'Dashboard/Dashboard.html'
    context_object_name = 'accepted_applications'
    def get_queryset(self):
        queryset = Apply_Job.objects.filter(status='Accepted')
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_accepted_applications'] = self.get_queryset().count()
        return context

class RejectedApplicationsView(ListView):
    model = Apply_Job
    template_name = 'Dashboard/Dashboard.html'
    context_object_name = 'rejected_applications'
    def get_queryset(self):
        queryset = Apply_Job.objects.filter(status='Rejected')
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_rejected_applications'] = self.get_queryset().count()
        return context

class PendingApplicationsView(ListView):
    model = Apply_Job
    template_name = 'Dashboard/Dashboard.html'
    context_object_name = 'pending_applications'
    def get_queryset(self):
        queryset = Apply_Job.objects.filter(status='Pending')
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_pending_applications'] = self.get_queryset().count()
        return context
# ----------------------------------------------

# class ReportsView(TemplateView):
#     template_name = 'Dashboard/Dashboard.html'
class ReportsView(ListView):
    template_name = 'Dashboard/Dashboard.html'
    context_object_name = 'counts_today'
    paginate_by = 10  

    def get_queryset(self):
        filter_type = self.request.GET.get('filter', 'today')
        user = self.request.user  
        today = timezone.now().date()
        end_date = today
        if filter_type == 'week':
            start_date = today - timedelta(days=today.weekday())
        elif filter_type == 'month':
            start_date = today.replace(day=1)
        elif filter_type == 'year':
            start_date = today.replace(month=1, day=1)
            end_date = today.replace(month=12, day=31)
        else:
            start_date = today
        counts = Apply_Job.objects.filter(
            job__company=user.company,
            timestamp__date__range=[start_date, end_date]
        ).values('status').annotate(count=Count('status'))
        return counts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_type = self.request.GET.get('filter', 'today')
        context['filter_title'] = filter_type.capitalize() 
        return context



# class JobseekerReportsView(TemplateView):
   
 
class JobseekerReportsView(TemplateView):
    template_name = 'Dashboard/Dashboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        filter_option = self.request.GET.get('filter', 'month')
        jobseeker = self.request.user
        if filter_option == 'today':
            start_date = today
            filter_title = "Today"
        elif filter_option == 'month':
            start_date = today.replace(day=1)
            filter_title = "This Month"
        elif filter_option == 'year':
            start_date = today.replace(month=1, day=1)
            filter_title = "This Year"
        else:
            start_date = today
            filter_title = "Today"
        counts = Apply_Job.objects.filter(
            user=jobseeker,
            timestamp__date__gte=start_date
        ).values('status').annotate(count=Count('id'))

        print(["Counts:", counts])

        context['counts'] = counts
        context['filter_title'] = filter_title
        return context
     

   


   


class RecentAppliedJobsListView(ListView):
    model = Apply_Job  
    template_name = 'Dashboard/Dashboard.html'
    context_object_name = 'recent_applied_jobs'

    def get_queryset(self):
        filter_option = self.request.GET.get('filter', 'month')
        queryset = Apply_Job.objects.filter(user=self.request.user)
        # queryset = Apply_Job.objects.filter(user=self.request.user).select_related('job__employer__user__profile')

        if filter_option == 'today':
            queryset = queryset.filter(timestamp__date=date.today())
            filter_option_text = 'Today'
        elif filter_option == 'this_month':
            queryset = queryset.filter(timestamp__month=date.today().month)
            filter_option_text = 'This Month'
        elif filter_option == 'this_year':
            queryset = queryset.filter(timestamp__year=date.today().year)
            filter_option_text = 'This Year'
        else:
            filter_option_text = 'All'  
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_option = self.request.GET.get('filter', 'today')
        if filter_option == 'today':
            filter_option_text = 'Today'
        elif filter_option == 'this_month':
            filter_option_text = 'This Month'
        elif filter_option == 'this_year':
            filter_option_text = 'This Year'
        else:
            filter_option_text = 'All'  
        context['filter_option'] = filter_option_text
        return context


class RecentlyPostedJobsListView(ListView):
    model = JobPost
    template_name = 'dashboard/Dashboard.html'
    context_object_name = 'recently_posted_jobs'
    def get_queryset(self):
        current_date = now().date()
        start_date = current_date - timedelta(days=7)  
        end_date = current_date + timedelta(days=1)   

        return JobPost.objects.filter(created_at__date__gte=start_date, created_at__date__lt=end_date)

class SekkerSearchAllJobsView(ListView):
    model = JobPost
    template_name = 'Job/search_all_job.html'
    # template_name = 'Job/seeker_view_job.html'

    def get_queryset(self):
            query = self.request.GET.get('search', '')
            location = self.request.GET.get('location', '')
            queryset = JobPost.objects.all()
            if query:
                queryset = queryset.filter(title__icontains=query)
            if location:
                queryset = queryset.filter(location__icontains=location)
            return queryset

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string(self.template_name, context)
            return JsonResponse({'html': html})
        else:
            return super().render_to_response(context, **response_kwargs)



# class DashboardView(View):
#     template_name = 'Dashboard/Dashboard.html'


# class TotalCountView(View):
# class TotalCountView(View):
class TotalCountView(View):
    def get(self, request, *args, **kwargs):
        filter_value = request.GET.get('filter', 'year')
        today = timezone.now().date()
        user = request.user  

        if filter_value == 'today':
            start_date = today
        elif filter_value == 'week':
            start_date = today - timedelta(days=today.weekday())
        elif filter_value == 'month':
            start_date = today.replace(day=1)
        elif filter_value == 'year':
            start_date = today.replace(month=1, day=1)
        elif filter_value == 'all':
            start_date = None
        else:
            start_date = None

        if start_date is not None:
            applications = Apply_Job.objects.filter(job__employer=user, timestamp__gte=start_date)
        else:
            applications = Apply_Job.objects.filter(job__employer=user)

        applied_users_count = applications.values('user').distinct().count()
        accepted_applications_count = applications.filter(status='Accepted').count()
        rejected_applications_count = applications.filter(status='Rejected').count()
        pending_applications_count = applications.filter(status='Pending').count()

        data = {
            'applied_users_count': applied_users_count,
            'accepted_applications_count': accepted_applications_count,
            'rejected_applications_count': rejected_applications_count,
            'pending_applications_count': pending_applications_count,
            'filter_title': filter_value.capitalize(),
        }

        return JsonResponse(data)

class TotalCountView(View):
    def get(self, request, *args, **kwargs):
        filter_value = request.GET.get('filter', 'year')
        today = timezone.now().date()
        employer = request.user  

        if filter_value == 'today':
            start_date = today
        elif filter_value == 'week':
            start_date = today - timedelta(days=today.weekday())
        elif filter_value == 'month':
            start_date = today.replace(day=1)
        elif filter_value == 'year':
            start_date = today.replace(month=1, day=1)
        elif filter_value == 'all':
            start_date = None
        else:
            start_date = None

        job_posts = JobPost.objects.filter(user=employer)

        total_applied_users = 0
        accepted_count = 0
        rejected_count = 0
        pending_count = 0
        recent_data = []

        for job_post in job_posts:
            applications = Apply_Job.objects.filter(job=job_post)
            if start_date:
                applications = applications.filter(timestamp__gte=start_date)

            total_applied_users += applications.values('user').distinct().count()
            accepted_count += applications.filter(status='Accepted').count()
            rejected_count += applications.filter(status='Rejected').count()
            pending_count += applications.filter(status='Pending').count()
            recent_applied_job = applications.select_related('job').values('job__title','user__username','timestamp')[:10]
            # for application in recent_applied_job :
            #    recent_data.append({
            #         'job_title': application['job__title'],
            #         'first_name': application['user__jobseeker_profile__first_name'],
            #         'last_name': application['user__jobseeker_profile__last_name'],
            #         'timestamp': application['timestamp'],
            #     })
            chart_data = {
            'labels': ['Accepted', 'Rejected', 'Pending'],
            'data': [accepted_count, rejected_count, pending_count],
        }

        data = {
            
            'applied_users_count': total_applied_users,
            'accepted_applications_count': accepted_count,
            'rejected_applications_count': rejected_count,
            'pending_applications_count': pending_count,
            'chart_data': chart_data,
            'filter_title': filter_value.capitalize(),
            'recently_applied_jobs': list(recent_applied_job),
        }

        return JsonResponse(data)








class TotalCountJobView(View):
    def get(self, request, *args, **kwargs):
        filter_value = request.GET.get('filter', 'year')
        today = timezone.now().date()
        jobseeker = request.user  

        if filter_value == 'today':
            start_date = timezone.make_aware(datetime.combine(today, datetime.min.time()))
        elif filter_value == 'week':
            start_date = timezone.make_aware(datetime.combine(today - timedelta(days=today.weekday()), datetime.min.time()))
        elif filter_value == 'month':
            start_date = timezone.make_aware(datetime.combine(today.replace(day=1), datetime.min.time()))
        elif filter_value == 'year':
            start_date = timezone.make_aware(datetime.combine(today.replace(month=1, day=1), datetime.min.time()))
        elif filter_value == 'all':
            start_date = None
        else:
            start_date = None


        total_application = 0
        accepted_count = 0
        rejected_count = 0
        pending_count = 0
      

       
        if start_date:
            applications = Apply_Job.objects.filter(user=jobseeker, timestamp__gte=start_date).order_by('-timestamp')
        else:
            applications = Apply_Job.objects.all(user=jobseeker).order_by('-timestamp')

        total_application += applications.count()
        accepted_count += applications.filter(status='Accepted').count()
        rejected_count += applications.filter(status='Rejected').count()
        pending_count += applications.filter(status='Pending').count()
        recent_applied_job = applications.select_related('job').values('job__title','user__username','timestamp')[:10]
        
        chart_data = {
                'labels': ['Accepted', 'Rejected', 'Pending'],
                'data': [accepted_count, rejected_count, pending_count],
                }

        data = {
            
            'all_application_count': total_application,
            'accepted_applications_counts': accepted_count,
            'rejected_applications_counts': rejected_count,
            'pending_applications_counts': pending_count,
            'chart_datas': chart_data,
            'filter_titles': filter_value.capitalize(),
            'recently_applied_jobs': list(recent_applied_job),
        }

        return JsonResponse(data)

# def send_message(request):
#     if request.method == 'POST':
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.sender = request.user
#             message.save()
#             return redirect('Mailbox')
#     else:
#         form = MessageForm()   
#     messages = Message.objects.filter(receiver=request.user)  
#     print(messages,"============================================")
#     context = {
#         'messages': messages,
#         'form': form,
#     }
#     return render(request, 'Dashboard/Dashboard.html', context)


def send_message(request):
    if request.method == 'POST':
        message_content = request.POST.get('message')
        recivern = request.POST.get('receiver')
        if message_content and recivern:
            receiver = User.objects.get(username=recivern)
            sender = request.user
            message = Message.objects.create(
                sender=sender,
                receiver=receiver,
                message=message_content
            )
            return JsonResponse({'status': 'success', 'message': 'Message sent successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid message data.'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)




def MailBox(request):
    user=request.user 
    messages=Message.objects.filter(sender=user) 
  
    for message in messages:
        if message.unread:
            message.unread=False
            message.save()
   
    context = {
        'messages':messages,
        
    }
    return render(request,'Dashboard/Emp_message.html',context)

def MailBoxid(request,pk):
    user=User.objects.get(pk=pk) 
    reciver = request.GET.get('receiver')
    messages=Message.objects.filter(sender=user) |  Message.objects.filter(receiver=reciver)
    
    for message in messages:
        if message.unread:
            message.unread=False
            message.save()
    context = {
        'messages':messages,
    }
    return render(request,'Dashboard/ChatEmo.html',context)


# def chat(request, pk):
#     if request.method == 'POST':
#         messages = request.POST.get('messages')
#         recivern = request.POST.get('pk')
#         if messages and recivern:
#             receiver = User.objects.get(username=recivern)
#             sender = request.user
#             message = Message.objects.create(
#                 sender=sender,
#                 receiver=receiver,
#                 message=messages
#             )
#             return JsonResponse({'status': 'success', 'message': 'Message sent'})
#         else:
#             return JsonResponse({'status': 'error', 'message': 'Invalid message data.'}, status=400)
#     elif request.method == "GET":
#         if recivern:
#             sender_username = request.user.username
#             messages = Message.objects.filter(
#                 sender__username__in=[sender_username, recivern],
#                 receiver__username__in=[sender_username, recivern]
#             ).order_by('-timestamp')
#             context = {
#                 "recivern": recivern,
#                 "messages": messages,
#             }
#             return render(request, 'Dashboard/chatEmo.html', context)
#         else:
#----------------------------------------------------------------------------------------------------------------#     

#-------------------------------Saved job by user---------------------------------------------------------------------#
# class SavedJobView(LoginRequiredMixin,View):
#     def post(self, request, Job_id  ,*args, **kwargs):
#         job =JobPost.objects.get(id=Job_id)
#         if not SavedJob.objects.filter(user = request.user , job = job):
#             SavedJob.objects.create(user=request.user,job = job)
#         return redirect('seeker_view_all_jobs')
class SavedJobView(LoginRequiredMixin, View):
    def post(self, request, Job_id, *args, **kwargs):
        try:
            job = JobPost.objects.get(id=Job_id)
            if not SavedJob.objects.filter(user=request.user, job=job).exists():
                SavedJob.objects.create(user=request.user, job=job)
        except JobPost.DoesNotExist:
            pass
        return redirect('saved_list')
class UnsavedView(LoginRequiredMixin, View):
    def post(self, request, Job_id, *args, **kwargs):
        job = JobPost.objects.get(id=Job_id)
        try:
            saved_job = SavedJob.objects.get(user=request.user, job=job)
            saved_job.delete()
        except SavedJob.DoesNotExist:
            pass  
        return redirect('saved_list')

        
    


class SavedListView(LoginRequiredMixin,ListView):
    model = SavedJob
    template_name = 'Job/Saved_jobs_List.html'
    context_object_name = 'saved_jobs'

    def get_queryset(self):
        return SavedJob.objects.filter(user = self.request.user).select_related('job')
    


class ReportJobView(CreateView):
    model = DisableJob
    form_class = DisableJobForm
    template_name = 'Job/report_job.html'
    def get_success_url(self):
        return reverse_lazy('seeker_view_all_jobs')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['job_id'] = self.kwargs.get('job_id')
        return kwargs

            



#-------------------------------report job by user-------------------------------------------------------------------#
      




      

  

 



