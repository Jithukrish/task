from django.contrib.auth import get_user_model
from django import forms
from UserApplicant.models import User
from chat.models import Thread,ChatMessage

class ThreadForm(forms.ModelForm):
    class Meta:
        model=Thread
        fields=['first_person', 'second_person']
       
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ThreadForm, self).__init__(*args, **kwargs)
        if user:
            print(f"User ID: {user.id}")
            self.fields['first_person'].queryset = User.objects.exclude(id=user.id)
            self.fields['second_person'].queryset = User.objects.exclude(id=user.id)
        else:
            print("No user passed")
            self.fields['first_person'].queryset = User.objects.all()
            self.fields['second_person'].queryset = User.objects.all()
        print(f"First Person Queryset: {self.fields['first_person'].queryset}")
        print(f"Second Person Queryset: {self.fields['second_person'].queryset}")

