from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Resume
from UserApplicant.models import User
from .forms import ResumeForm
from django.views.generic import FormView,View



# class ResumeUploadView(FormView):
#     template_name="Resume/Update_resume.html"
#     form_class=ResumeForm

#     def get(self,request):
#         if not request.user.is_authenticated or not request.user.is_jobseeker:
#             messages.warning(request, 'Permission denied.')
#             return redirect('Seeker_home')
#         try:
#             resume = Resume.objects.get(user=request.user)
#             form = self.form_class(request.POST, request.FILES, instance=resume)
#         except Resume.DoesNotExist:
#             form = self.form_class(request.POST, request.FILES)
        
#         context = {
#             'form': form
#         }
#         return render(request, self.template_name, context)
#     def post(self,request, *args, **kwargs):
#             if not request.user.is_authenticated or not request.user.is_jobseeker:
#                 messages.warning(request, 'Permission denied.')
#                 return redirect('Seeker_home')

#             try:
#                 resume = Resume.objects.get(user=request.user)
#                 form = self.form_class(request.POST, request.FILES, instance=resume)
#             except Resume.DoesNotExist:
#                 form = self.form_class(request.POST, request.FILES)
#             if form.is_valid():
#                 resume = form.save(commit=False)
#                 resume.user = request.user  
#                 resume.save()
                
#                 messages.success(request, 'Resume updated successfully.')
#                 return redirect('jobseeker_dash')
#             else:
#                 messages.error(request, 'Error updating resume.')
          
#             context = {
#                 'form': form
#             }
#             return render(request, 'resume/update_resume.html', context)


class ResumeUploadView(View):
    template_name = "Resume/update_resume.html"
    form_class = ResumeForm

    def get_object(self):
        try:
            return Resume.objects.get(user=self.request.user)
        except Resume.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_jobseeker:
            messages.warning(request, 'You do not have permission to update your resume.', extra_tags='resume_update')
            return redirect('jobseeker_dash')
        
        resume = self.get_object()
        form = self.form_class(instance=resume)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_jobseeker:
            messages.warning(request, 'You do not have permission to update your resume.')
            return redirect('jobseeker_dash')
        
        resume = self.get_object()
        form = self.form_class(request.POST, request.FILES, instance=resume)
        
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user  
            resume.save()
            messages.success(request, 'Resume updated successfully.', extra_tags='resume_update')
            return redirect('update_resume')
        else:
            messages.error(request, 'Error updating resume.', extra_tags='resume_update')
        
        context = {'form': form}
        return render(request, self.template_name, context)


    

            
         
  
                
from django.views.generic import DetailView        

class ResumeView(DetailView):
    model=Resume
    template_name='resume/resume_details.html'
    context_object_name='resume'
    pk_url_kwarg = 'id'



    
