from django.contrib.auth import get_user_model
from django import forms
from UserApplicant.models import User
from chat.models import Thread,ChatMessage

class ThreadForm(forms.ModelForm):
    class Meta:
        model=Thread
        fields=['first_person', 'second_person']
       
    def __init__(self, *args, **kwargs):
        super(ThreadForm, self).__init__(*args, **kwargs)
        self.fields['first_person'].queryset = User.objects.all()
        self.fields['second_person'].queryset = User.objects.all()

# class ChatMessageForm(forms.ModelForm):
#     class Meta:
#         model = ChatMessage
#         fields = ['phone_number','address','about','profile_picture','first_name','last_name','date_of_birth','gender','education', 'job', 'country', 'skills', 'x', 'facebook', 'linkedin','insta']
#         widgets = {
#                     'skills': forms.CheckboxSelectMultiple,
#                 }