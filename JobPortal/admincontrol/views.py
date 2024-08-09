from datetime import date, timezone
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from Job.models import Apply_Job, JobPost
from Company.models import Company
from admincontrol.models import AddImg, Address_contact, Companylogo, Contact_Main, Contact_contact, FeaturesTab1, FeaturesTab2, FeaturesTab3, Featuresub, Frequently_asked, Head, IconServices, Mail_contact,Menu, Section1, SelectedJob,Aboutus, Service, Socialmedia
from .forms import CompanyForm, ContactSectionForm, ContactSectionMainForm, FeatureTabFiveForm, FeatureTabSecondForm, FeaturesTab1Form, FeaturesubForm, FrequentlyAskedForm, HeaderForm,HeaderMenuForm,SectionForm, SelectJobForm, AboutForm, ServiceForm, SocialmediaForm
from django.views.generic.edit import FormView,CreateView,View
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView 
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count
from django.views.generic import DeleteView
from django.utils import timezone
import datetime
from datetime import datetime
from datetime import datetime, timedelta   
from django.utils.timezone import now
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
User = get_user_model()
    

class HeaderFormView(CreateView):
    model =Head
    template_name = "admin/header.html"
    form_class = HeaderForm
    success_url =reverse_lazy('admin_dash')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
class HeaderEditView(UpdateView):
    model=Head
    template_name = 'admin/haederedit.html'
    fields = ['name','title','logo_img']
    success_url = reverse_lazy('admin_dash')    
    context_object_name='card'

    def form_valid(self,form):
        response = super().form_valid(form)
        messages.success(self.request, 'Updated Successfully')
        return response
    def form_invalid(self, form):
        print(form.errors)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('menu_list')  

class HeaderlistView(ListView):
    model=Head
    template_name='admin/edithead.html'
    context_object_name='menu'

class MenuCreateView(View):
    def post(self, request, *args, **kwargs):
        menu_name = request.POST.get('menu_name')
        if menu_name:
            menu_item = Menu.objects.create(menu_item=menu_name)
            response = {
                'name': menu_item.menu_item
            }
            return JsonResponse(response)
        else:
            return JsonResponse({'error': 'No Name here'}, status=400)
        
class MenuUpdateView(ListView):
    model=Menu
    template_name='admin/editmenu.html'
    context_object_name='menu'

class MenuEditView(UpdateView):
    model=Menu
    template_name = 'admin/Menuedit.html'
    fields = ['menu_item','menu_url']
    success_url = reverse_lazy('admin_dash')    
    context_object_name='card'

    def form_valid(self,form):
        response = super().form_valid(form)
        messages.success(self.request, 'Updated Successfully')
        return response
    def form_invalid(self, form):
        print(form.errors)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('menu_list') 

class MenuDeleteView(View):
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        menu = Menu.objects.get(pk=pk)
        menu.delete()
        return JsonResponse({'message': 'Item deleted successfully'})
    

# class ServiceDeleteView(View):
#     def post(self, request, *args, **kwargs):
#         pk = self.kwargs.get('pk')
#         service = Service.objects.get(id=pk)
#         service.delete()
#         return JsonResponse({'message': 'Service deleted successfully'})
    

 
#------------------------------------------------section1-----------------------------------------------
class SectionView(CreateView):
    model =Section1
    template_name = "admin/section1.html"
    form_class = SectionForm
    success_url =reverse_lazy('admin_dash')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    def form_invalid(self, form):
        print(form.errors)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
        return super().form_invalid(form)
    




class SelectJobsForUserView(FormView):
    template_name = 'admin/selectjob.html'
    form_class = SelectJobForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.kwargs['user_id']
        return kwargs

    def get_initial(self):
        return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs['user_id']
        context['user'] = User.objects.get(pk=user_id)
        context['jobs'] = JobPost.objects.all()
        return context

    def form_valid(self, form):
        user = User.objects.get(pk=self.kwargs['user_id'])
        selected_jobs = form.cleaned_data['jobs']
        SelectedJob.objects.filter(user=user).delete()
        for job in selected_jobs:
            SelectedJob.objects.create(user=user, job=job)
        return super().form_valid(form)
    def form_invalid(self, form):
        print(form.errors)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
        return super().form_invalid(form)

    def get_success_url(self):
        user_id = self.kwargs['user_id']
        return reverse_lazy('selected_jobs', kwargs={'user_id': user_id})

# def selected_jobs(request, user_id):
#     user = User.objects.get(pk=user_id)
#     selected_jobs = SelectedJob.objects.filter(user=user)
#     return render(request, 'admin/selected_jobs.html', {'selected_jobs': selected_jobs, 'user': user})
class UserDetailView(DetailView):
    model = User
    template_name = 'admin/selected_jobs.html'
    context_object_name = 'user'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['selected_jobs'] = SelectedJob.objects.filter(user=user)
        return context
 #------------------------------------------------section1-----------------------------------------------


class AboutUsFormView(CreateView):
# class AboutUsFormView(BaseFormView):
    model = Aboutus
    template_name = "admin/aboutus.html"
    form_class = AboutForm
    success_url=reverse_lazy('admin_dash')
    def form_valid(self, form):
        print(form.cleaned_data)
        form.save() 
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
        return super().form_invalid(form)
    
class AboutUsEditView(UpdateView):
# class AboutUsEditView(BaseFormView):
    model = Aboutus
    form_class = AboutForm
    template_name = "admin/aboutus.html"
    success_url=reverse_lazy('admin_dash')

# from django.views.generic.edit import ModelFormMixin
# class BaseFormView(ModelFormMixin, View):
#     model = Aboutus
#     form_class = AboutForm
#     template_name = "admin/aboutus.html"
#     success_url=reverse_lazy('admin_dash')
#     def get(self, request, *args, **kwargs):
#         instance = self.get_object() if self.kwargs.get('pk') else None
#         form = self.get_form(instance=instance)
#         return render(request, self.template_name, {'form': form})

#     def post(self, request, *args, **kwargs):
#         instance = self.get_object() if self.kwargs.get('pk') else None
#         form = self.get_form(instance=instance)
#         if form.is_valid():
#             form.save()
#             return redirect(self.success_url)
#         return render(request, self.template_name, {'form': form})

#     def get_form(self, instance=None):
#         if instance:
#             return self.form_class(instance=instance, data=self.request.POST, files=self.request.FILES)
#         return self.form_class(data=self.request.POST, files=self.request.FILES)

#     def get_object(self):
#         if self.kwargs.get('pk'):
#             return self.model.objects.get(pk=self.kwargs['pk'])
#         return None




class ImageView(View):
    def post(self, request, *args, **kwargs):
        About_img = request.FILES.get('About_img')
        if About_img:
            About_img = AddImg.objects.create(About_img=About_img)
            response = {
                'img_url': About_img.About_img.url
            }
            return JsonResponse(response)
        else:
            return JsonResponse({'error': 'pls upload file'}, status=400)
        


class CompanyFormView(CreateView):
    model = Companylogo
    template_name = "admin/Companylogo.html"
    form_class = CompanyForm
    success_url=reverse_lazy('all_comoany_logo')
    def form_valid(self, form):
        print(form.cleaned_data)
        form.save() 
        messages.success(self.request, 'Send Successfully ')
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)
    
class CompanyLogoDetailview(ListView):
    model = Companylogo
    template_name = 'admin/Companylogodetail.html'
    context_object_name = 'companylogo'



class CompanyLogoUpdateView(UpdateView):
    model=Companylogo
    fields = ['logo','logo_name']
    template_name = 'admin/companylogoupdate.html'
    success_url = reverse_lazy('admin_dash')    
    context_object_name='card'

    def form_valid(self,form):
        response = super().form_valid(form)
        messages.success(self.request, 'Updated Successfully')
        return response

    def get_success_url(self):
        return reverse_lazy('all_comoany_logo') 

class FeatureFormView(CreateView):
    model = FeaturesTab1
    template_name = "admin/Featuresub.html"
    form_class = FeaturesTab1Form
    success_url=reverse_lazy('admin_dash')
    def form_valid(self, form):
        print(form.cleaned_data)
        form.save() 
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)
    

class SubfeatureView(View):
    def post(self, request, *args, **kwargs):
        sub_title = request.POST.get('title','description')
        # sub_description = request.POST.get('description')
        
        if sub_title:
            title_add = Featuresub.objects.create(title=sub_title,description=sub_title)
            response = {
                'name': title_add.title,
                'description':title_add.description
            }
            return JsonResponse(response)
        else:
            return JsonResponse({'error': 'No title found'}, status=400)
        




class TabSecondFormView(CreateView):
    model = FeaturesTab2
    template_name = "admin/TabSecondFormView.html"
    form_class = FeatureTabSecondForm
    success_url=reverse_lazy('admin_dash')
    def form_valid(self, form):
        print(form.cleaned_data)
        form.save() 
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)



class TabThirdFormView(CreateView):
    model = FeaturesTab3
    template_name = "admin/TabThirdFormView.html"
    form_class = FeatureTabFiveForm
    success_url=reverse_lazy('section_five')
    def form_valid(self, form):
        print(form.cleaned_data)
        form.save() 
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)
    


class SectionFiveUpdateView(UpdateView):
    model=FeaturesTab3
    fields=['image','description','field','title']
    template_name = "admin/TabThirdFormUpdateView.html"
    success_url = reverse_lazy('section_five')    
    context_object_name='card'

    def form_valid(self,form):
        response = super().form_valid(form)
        messages.success(self.request, 'Updated Successfully')
        return response

    def get_success_url(self):
        return reverse_lazy('admin_dash')
    

#----------------------------------service---------------------------------

class ServiceView(CreateView):
    model = Service
    template_name = "admin/Service.html"
    form_class = ServiceForm
    success_url=reverse_lazy('all_service')
    def form_valid(self, form):
        print(form.cleaned_data)
        form.save() 
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)



class ServiceiconView(View):
    def post(self, request, *args, **kwargs):
        icon_ch = request.POST.get('icon')
        if icon_ch:
            icon_ch = IconServices.objects.create(icon=icon_ch)
            response = {
                'icon_check': icon_ch.icon
            }
            return JsonResponse(response)
        else:
            return JsonResponse({'error': 'Add icon text'}, status=400)
        

class ServiceAllView(ListView):
    model = Service
    template_name = 'admin/serviceall.html'
    context_object_name ='services'


class ServiceUpdateView(UpdateView):
    model=Service
    fields = ['title','description','icons']
    template_name = 'admin/serviceupdate.html'
    success_url = reverse_lazy('all_service')    
    context_object_name='card'

    def form_valid(self,form):
        response = super().form_valid(form)
        messages.success(self.request, 'Updated Successfully')
        return response

    def get_success_url(self):
        return reverse_lazy('all_service') 
    


# class ServiceDeleteView(DeleteView):
class ServiceDeleteView(View):
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        service = Service.objects.get(id=pk)
        service.delete()
        return JsonResponse({'message': 'Service deleted successfully'})
    


class ContactSectionView(CreateView):
    model = Contact_Main
    template_name = "admin/ContactSectionView.html"
    form_class = ContactSectionMainForm
    success_url=reverse_lazy('admin_dash')
    def form_valid(self, form):
        print(form.cleaned_data)
        form.save() 
        return super().form_valid(form)
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)



    



class AddressView(View):
    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        address = request.POST.get('address')
        ad_icon = request.POST.get('ad_icon')
        if title and address and ad_icon:
            icon_ch = Address_contact.objects.create(title=title,address=address,ad_icon=ad_icon)
            response = {
                'address': icon_ch.address,
                'title': icon_ch.title,
                'adicon': icon_ch.ad_icon,
                
            }
            return JsonResponse(response)
        else:
            return JsonResponse({'error': 'ERERER'}, status=400)
        
class ContactView(View):
    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        phone = request.POST.get('phone')
        ad_icon = request.POST.get('ad_icon')
        if title and phone and ad_icon:
            icon_ch = Contact_contact.objects.create(title=title,phone=phone,ad_icon=ad_icon)
            response = {
                'phone': icon_ch.phone,
                'title': icon_ch.title,
                'adicon': icon_ch.ad_icon,
                
            }
            return JsonResponse(response)
        else:
            return JsonResponse({'error': 'ERERER'}, status=400)
class MailView(View):
    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        email = request.POST.get('email')
        ad_icon = request.POST.get('ad_icon')
        if title and email and ad_icon:
            icon_ch = Mail_contact.objects.create(title=title,email=email,ad_icon=ad_icon)
            response = {
                'email': icon_ch.email,
                'title': icon_ch.title,
                'adicon': icon_ch.ad_icon,
                
            }
            return JsonResponse(response)
        else:
            return JsonResponse({'error': 'ERERER'}, status=400)
          
# class ContactSectionView(CreateView):
class FrequentSectionView(CreateView):
    # model = Contact_Main
    template_name = "admin/frequentlyasked.html"
    form_class = FrequentlyAskedForm
    success_url=reverse_lazy('admin_dash')
    def form_valid(self, form):
        print(form.cleaned_data)
        question = form.cleaned_data.get('question')
        if Frequently_asked.objects.filter(question=question).exists():
            form.add_error('question', 'This question already exists.')
            return self.form_invalid(form) 
        
        else:
            form.save()
            return JsonResponse({'success': True})

    def form_invalid(self, form):
        print(form.errors)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
       
        return super().form_invalid(form)
    
class FrequencyListView(ListView):
    model = Frequently_asked
    template_name="admin/frequencyList.html"
    context_object_name='frequently_asked'


class frequentlyUpdateView(UpdateView):
    model = Frequently_asked
    fields =['question','answer']
    template_name = 'admin/frequentlyupdate.html'
    success_url = reverse_lazy('frequency_asked_list')




class frequentDeleteView(View):
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        try:
            faq = Frequently_asked.objects.get(pk=pk)
            faq.delete()
            return JsonResponse({'message': 'question deleted successfully'})
        except Frequently_asked.DoesNotExist:
            return JsonResponse({'error': 'question  does not exist'}, status=404)


class RestrictUserView(TemplateView):
    model = User
    template_name = 'admin/restrict_user.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all().exclude(is_superuser=True)
        return context
    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        user.is_active = not user.is_active 
        user.save()
        status = 'active' if user.is_active else 'inactive'
        messages.success(request, f"User status updated to {status}.")
        return redirect('admin_dash')


class JobRestrictView(TemplateView):
    model=JobPost
    template_name='admin/job_restrict.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["jobs"] = JobPost.objects.all()
        return context
    def post(self, request, *args, **kwargs):
        job_id = request.POST.get('job_id')
        try:
            Job = JobPost.objects.get(id=job_id)
        except JobPost.DoesNotExist:
            Job = None
        Job.is_active =not Job.is_active
        Job.save()
        status = 'active' if Job.is_active else 'deactive'
        messages.success(request,f"status updated successfully {status}")
        return redirect('admin_dash')
    


class CompanyRestrictView(TemplateView):
    models=Company
    template_name ='admin/Company_restrict.html'
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        context['companies']=Company.objects.all()
        return context
    def post(self,request,*args, **kwargs):
        company_id=request.POST.get('company_id')
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            company = None
        company.is_active =not company.is_active
        company.save()
        status = 'active' if company.is_active else 'Deactivate'
        messages.success(request,f'company status changed {status}')
        return redirect('admin_dash')
    



class socialmediaView(CreateView):
    template_name = 'admin/Socialmedia.html'
    form_class = SocialmediaForm
    success_url=reverse_lazy('admin_dash')
    def form_valid(self, form):
        # print(form.cleaned_data)
        form.save() 
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
        return super().form_invalid(form)
    
class socialmediaListview(ListView):
    model = Socialmedia
    template_name = 'admin/socialmedia_list.html'
    context_object_name ='socialmedia'




class socialmediaUpdateView(UpdateView):
    model = Socialmedia
    fields =['title','url_icon']
    template_name = 'admin/socialmedia_update.html'
    success_url = reverse_lazy('social_media_list')




class socialDeleteView(View):
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        try:
            service = Socialmedia.objects.get(pk=pk)
            service.delete()
            return JsonResponse({'message': 'social deleted successfully'})
        except Socialmedia.DoesNotExist:
            return JsonResponse({'error': 'Social media does not exist'}, status=404)

from django.db.models import Q


class AdvancesearchView(ListView):
    model = JobPost
    template_name = "admin/advance_search_result.html"
    context_object_name = 'job_result'

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        location_query = self.request.GET.get('location', '')
        job_type_query = self.request.GET.get('job_type', '')

        jobs = JobPost.objects.all()  
        print(location_query)
        print(search_query)

        if search_query:
            jobs = jobs.filter(
                Q(title__icontains=search_query) |
                Q(skills__name__icontains=search_query) |
                Q(company__name__icontains=search_query)
            )
        if location_query:
            jobs = jobs.filter(
                Q(location__icontains=location_query)
            )
        if job_type_query:
            jobs = jobs.filter(
                Q(job_type__icontains=job_type_query)
            )

        return jobs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['location_query'] = self.request.GET.get('location', '')
        context['job_type_query'] = self.request.GET.get('job_type', '')
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
           # return render(self.request,'admin/advance_search_result.html',context) 
            html = render_to_string('admin/advance_search_result.html', context,request=self.request )
            return JsonResponse({'html': html})
        return super().render_to_response(context, **response_kwargs)


   













class AdminTotalCountJobView(View):
    def get(self, request, *args, **kwargs):
        filter_value = request.GET.get('filter', 'year')
        today = timezone.now().date()
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
        total_employer=0
        total_jobseeker=0
        accepted_count = 0
        rejected_count = 0
        pending_count = 0
      

       
        if start_date:
            applications = Apply_Job.objects.filter( timestamp__gte=start_date).order_by('-timestamp')
        else:
            applications = Apply_Job.objects.all().order_by('-timestamp')

        total_application += applications.count()
        total_employer+=applications.values('job__company__user').distinct().count()
        total_jobseeker+=applications.values('job__user').distinct().count()
        # print("+++++++++++++total_employer+++++++++++",total_employer)
        # print("+++++++++++++total_jobseeker+++++++++++",total_employer)
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
            'all_employer': total_employer,
            'all_jobseeker': total_jobseeker,
            'accepted_applications_counts': accepted_count,
            'rejected_applications_counts': rejected_count,
            'pending_applications_counts': pending_count,
            'chart_datas': chart_data,
            'filter_titles': filter_value.capitalize(),
            'recently_applied_jobs': list(recent_applied_job),
        }

        return JsonResponse(data)
