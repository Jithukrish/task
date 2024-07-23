from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Profile,jobseeker_Profile
class RegisterUserForm(UserCreationForm):
  
    class Meta:
        model=get_user_model()
        fields=['email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect(), required=False)


    class Meta:
        model = Profile
        fields = ['first_name','last_name','about','phone_number','address','profile_picture','gender','date_of_birth','education', 'job', 'country', 'skills','insta', 'x', 'facebook', 'linkedin']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] ='Enter your first name'
        self.fields['last_name'].widget.attrs['placeholder'] ='Enter your last name'
        self.fields['phone_number'].widget.attrs['placeholder'] ='Enter your phone number'
        self.fields['address'].widget.attrs['placeholder'] ='Enter your address'

from django.contrib.auth.forms import PasswordChangeForm

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'id': 'currentPassword'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'id': 'newPassword'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'id': 'renewPassword'})
class jobseekerProfileForm(forms.ModelForm):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect(),required=False)
    class Meta:
        model = jobseeker_Profile
        fields = ['phone_number','address','about','profile_picture','first_name','last_name','date_of_birth','gender','education', 'job', 'country', 'skills', 'x', 'facebook', 'linkedin','insta']
        widgets = {
                    'skills': forms.CheckboxSelectMultiple,
                }