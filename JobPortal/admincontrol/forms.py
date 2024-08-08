from django.contrib.auth import get_user_model
from django import forms
from Job.models import JobPost
from contact.models import Contact
from admincontrol.models import Address_contact, Companylogo, Contact_Main, Contact_contact, FeaturesTab1, FeaturesTab2, FeaturesTab3, Frequently_asked, Head, IconServices, Mail_contact,Menu,Section1,Aboutus,Featuresub,AddImg, Service, Socialmedia
from UserApplicant.models import User

class HeaderForm(forms.ModelForm):
    class Meta:
        model=Head
        fields=['title','logo_img','name']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].queryset = Menu.objects.all()
        
class HeaderMenuForm(forms.ModelForm):
    class Meta:
        model=Menu
        fields=['menu_item','menu_url']



class SectionForm(forms.ModelForm):
    class Meta:
        model=Section1
        fields=['description','img']


class SelectJobForm(forms.Form):
    jobs = forms.ModelMultipleChoiceField(
        queryset=JobPost.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user_id:
            self.fields['jobs'].queryset = JobPost.objects.all()#filter job based user


class AboutForm(forms.ModelForm):
    About_img = forms.ModelMultipleChoiceField(
        queryset=AddImg.objects.all(),
        required=False,
        widget=forms.SelectMultiple   
    )
    class Meta:
        model = Aboutus
        fields = ['title', 'img', 'description', 'element1', 'element2', 'element3']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['img'].queryset = AddImg.objects.all()
class AboutImgForm(forms.ModelForm):
    class Meta:
        model=AddImg
        fields=['About_img']



class CompanyForm(forms.ModelForm):
    class Meta:
        model=Companylogo
        fields=['logo','logo_name']


class FeaturesubForm(forms.ModelForm):
    class Meta:
        model=Featuresub
        fields=['title','description']

class FeaturesTab1Form(forms.ModelForm):
    subfeature = forms.ModelMultipleChoiceField(
        queryset=Featuresub.objects.all(),
        widget=forms.SelectMultiple,
        required=True
    )
    class Meta:
        model=FeaturesTab1
        fields=['subfeature','images']
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['subfeature'].queryset = Featuresub.objects.all()


class FeatureTabSecondForm(forms.ModelForm):
    class Meta:
        model=FeaturesTab2
        fields=['title','description','image']

class FeatureTabFiveForm(forms.ModelForm):
    class Meta:
        model=FeaturesTab3
        fields=['image','description','field','title']



class ServicesubForm(forms.ModelForm):
    class Meta:
        model=IconServices
        fields=['icon']

class ServiceForm(forms.ModelForm):

    class Meta:
        model=Service
        fields=['title','icons','description']
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['icons'].queryset = IconServices.objects.all()

class ContactSectionMainForm(forms.ModelForm):
    class Meta:
        model=Contact_Main
        fields=['add_main','cont_main','mail_main']
       
    # def __init__(self, *args, **kwargs):
    #         super().__init__(*args, **kwargs)
    #         self.fields['add_main'].queryset = Address_contact.objects.all()
class AddressSectionForm(forms.ModelForm):
    class Meta:
        model=Address_contact
        fields=['title','address','ad_icon']
class ContactSectionForm(forms.ModelForm):
    class Meta:
        model=Contact_contact
        fields=['title','phone','ad_icon']
class MailSectionForm(forms.ModelForm):
    class Meta:
        model=Mail_contact
        fields=['title','email','ad_icon']



class FrequentlyAskedForm(forms.ModelForm):
    class Meta:
        model=Frequently_asked
        fields=['question','answer']
       
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['question'].queryset = Contact.objects.all()

class SocialmediaForm(forms.ModelForm):
    class Meta:
        model = Socialmedia
        fields=['title','url_icon',]