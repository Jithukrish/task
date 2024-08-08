import datetime
from datetime import datetime
from django.db import models
from Job.models import JobPost
from django.contrib.auth import get_user_model

from contact.models import Contact
User = get_user_model()

   
class Menu(models.Model):
    menu_item = models.CharField(max_length=50,blank=True,null=True)
    menu_url = models.CharField(max_length=200,default='')
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.menu_item

class Head(models.Model):
    name = models.ManyToManyField(Menu,related_name='head_set')
    title = models.CharField(max_length=20,blank=True,null=True)
    logo_img = models.ImageField(upload_to='Header/',blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
         return self.title if self.title else "..."
class Section1(models.Model):
    description =models.TextField()
    img = models.ImageField(upload_to='Header/',blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)


class AddImg(models.Model):
    About_img = models.ImageField(upload_to='About/',blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        if self.About_img:
            return self.About_img.url
        return "....."
class Aboutus(models.Model):
    img= models.ManyToManyField(AddImg)
    title =models.CharField(max_length=200,blank=True,null=True)
    description =models.TextField()
    element1 = models.CharField(max_length=200,blank=True,null=True)
    element2 = models.CharField(max_length=200,blank=True,null=True)
    element3 = models.CharField(max_length=200,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)
class Companylogo(models.Model):
    logo = models.ImageField(upload_to='CompanyLogo/',blank=True,null=True)
    logo_name =models.CharField(max_length=100, blank=True,null=True,default='add name')
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        if self.logo:
            return self.logo.url
        return "....."
            
class Featuresub(models.Model):
    title =models.CharField(max_length=200,blank=True,null=True)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
class FeaturesTab1(models.Model):
    subfeature=models.ManyToManyField(Featuresub)
    images =models.ImageField(upload_to='Features/',blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.Featuresub.title

class FeaturesTab2(models.Model):
    title =models.CharField(max_length=200,blank=True,null=True)
    description =models.TextField()
    image = models.ImageField(upload_to='Features/',blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class FeaturesTab3(models.Model):
    title =models.CharField(max_length=200,blank=True,null=True)
    field = models.CharField(max_length=255,blank=True,null=True)
    description =models.TextField()
    image = models.ImageField(upload_to='Features/',blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.Featuresub.title

class IconServices(models.Model):
    icon = models.CharField(max_length=200,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.icon
class Service(models.Model):
    
    title = models.CharField(max_length=255,blank=True,null=True)
    icons=models.ForeignKey(IconServices,on_delete=models.CASCADE,blank=True,null=True,default="")
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    


class Address_contact(models.Model):
    title=models.CharField(max_length=200,blank=True,null=True)
    address = models.CharField(max_length=200,blank=True,null=True)
    ad_icon =models.CharField(max_length=50,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
class Contact_contact(models.Model):
    title=models.CharField(max_length=200,blank=True,null=True)
    phone = models.CharField(max_length=12)
    ad_icon =models.CharField(max_length=50,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
class Mail_contact(models.Model):
    title=models.CharField(max_length=200,blank=True,null=True)
    email = models.EmailField(max_length=200,blank=True,null=True)
    ad_icon =models.CharField(max_length=50,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Contact_Main(models.Model):
    add_main=models.ForeignKey(Address_contact,on_delete=models.CASCADE,blank=True,null=True)
    cont_main=models.ForeignKey(Contact_contact,on_delete=models.CASCADE,blank=True,null=True)
    mail_main=models.ForeignKey(Mail_contact,on_delete=models.CASCADE,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Main Contact: {self.add_main}"



class Frequently_asked(models.Model):
    question = models.ForeignKey(Contact,on_delete=models.CASCADE)
    answer = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"question: {self.question}"

class SelectedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'job')  
    def __str__(self):
        return f'{self.user} selected {self.job.title}'
    
class Socialmedia(models.Model):
    title = models.CharField(max_length=200,blank=True,null=True)
    url_icon=models.URLField(max_length=200,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"title: {self.title}"