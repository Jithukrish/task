from django import forms
from .models import JobPost,Education,Skills_job,Apply_Job,SalaryRange
from Company.models import Company

# class JobPostForm(forms.ModelForm):
#     class Meta:
#         model=JobPost
#         exclude=('user',)
#         widgets = {
#                     'skills': forms.CheckboxSelectMultiple,
#                 }
class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['name']

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skills_job
        fields = ['name']
class SalaryRangeForm(forms.ModelForm):
    class Meta:
        model = SalaryRange
        fields = ['salary_range']

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        exclude = ('user',)
       
        widgets = {
            'skills': forms.CheckboxSelectMultiple,
        }
    education_form = EducationForm()
    salary_form = SalaryRangeForm()

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user.is_authenticated and user.is_employer:
            self.fields['company'].queryset = Company.objects.filter(user=user)
        else:
            self.fields['company'].queryset = Company.objects.none()

    
       
   
       

class UpdateJobPostForm(forms.ModelForm):
    class Meta:
        model=JobPost
        exclude=('user',)

  
# class ApplyJobForm(forms.ModelForm):
#     cover_letter = forms.FileField(label='Upload cover letter', required=False)
#     resume = forms.FileField(label='Upload Resume', required=False)

#     class Meta:
#         model = Apply_Job
#         fields = ['resume', 'cover_letter']


class ApplyJobForm(forms.ModelForm):

    class Meta:
        model = Apply_Job
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs.pop('user', None)  
     
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model   = Message
        fields  =[
            'sender',
            'receiver',
            'message',
        ] 