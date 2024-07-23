from django.shortcuts import redirect, render
from django.contrib import messages
from django.views import View
from .models import Company
from UserApplicant.models import User
from .forms import UpdateCompanyForm
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

class AddComapnyDetailsView(LoginRequiredMixin, UpdateView):
    model=Company
    form_class=UpdateCompanyForm
    template_name='Company/update_company.html'
    success_url = 'company/update_company/'
    def get(self, request):
        if not  request.user.is_authenticated or not request.user.is_employer:
            messages.warning(request, 'Permission denied.')
            return redirect('jobseeker_dash')

        try:
            company = Company.objects.get(user=request.user)
        except Company.DoesNotExist:
            company = Company(user=request.user)

      
        form = self.form_class(instance=company)

        context = {
            'form': form,
            'company': company,
        }
        return render(request, self.template_name, context)   
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_employer:
            messages.warning(request, 'Permission denied.',extra_tags='update_company')
            return redirect('jobseeker_dash')

        try:
            company = Company.objects.get(user=request.user)
        except Company.DoesNotExist:
            company = Company(user=request.user)
        
        form = UpdateCompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            user = request.user
           
            user.save()
            messages.info(request, 'Your data has been updated successfully.',extra_tags='update_company')
            return redirect('create_job_post')
        else:
            messages.warning(request, 'Something went wrong. Please check the form.',extra_tags='update_company')
    

        context = {
            'form': form
        }
        return render(request, 'company/update_company.html', context)

     
# def update_company(request):
#     if not request.user.is_authenticated or not request.user.is_employer:
#         messages.warning(request, 'Permission denied.')
#         return redirect('jobseeker_dash')

#     try:
#         company = Company.objects.get(user=request.user)
#     except Company.DoesNotExist:
#         company = Company(user=request.user)

#     if request.method == 'POST':
#         form = UpdateCompanyForm(request.POST, request.FILES, instance=company)
#         if form.is_valid():
#             form.save()
#             user = request.user
           
#             user.save()
#             messages.info(request, 'Your data has been updated successfully.')
#             return redirect('update_company')
#         else:
#             messages.warning(request, 'Something went wrong. Please check the form.')
#     else:
#         form = UpdateCompanyForm(instance=company)

#     context = {
#         'form': form
#     }
#     return render(request, 'company/update_company.html', context)


# def update_company(request):
#     if request.user.is_authenticated and request.user.is_employer:
#         try:
#             company = Company.objects.get(user=request.user)
#         except Company.DoesNotExist:
#             messages.warning(request, 'Company profile does not exist.')
#             return redirect('jobseeker_dash')

#         if request.method == 'POST':
#             form = UpdateCompanyForm(request.POST, instance=company)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, 'Your company details have been updated successfully.')
#                 return redirect('jobseeker_dash')
#             else:
#                 messages.warning(request, 'Something went wrong. Please check the form.')
#         else:
#             form = UpdateCompanyForm(instance=company)

#         context = {
#             'form': form
#         }
#         return render(request, 'company/update_company.html', context)
#     else:
#         messages.warning(request, 'Permission denied.')
#         return redirect('jobseeker_dash')

      
#job creation employer

# def company_detail(request, id):
#     company=Company.objects.get(id=id)
#     context={
#         'company':company
#     }
#     return render(request, 'company/company_detail.html', context)


class CompanyDetailsView(DetailView):
    model = Company
    template_name = "company/company_detail.html"
    context_object_name='company'
    pk_url_kwarg = 'id'
     