from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_employer=models.BooleanField(default=False)
    is_jobseeker=models.BooleanField(default=False)
    has_resume=models.BooleanField(default=False)
    has_company=models.BooleanField(default=False)
    is_verified =models.BooleanField(default=False)
    verification_token= models.CharField(max_length=64,unique=True,blank=True)
    is_blocked =models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.verification_token:
            self.verification_token = get_random_string(length=32)
        super().save(*args, **kwargs)
#model of employer profile
class Profile(models.Model):
    user =models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=15,blank=True, null=True)
    address=models.CharField(max_length=255,blank=True,null=True)
    profile_picture=models.ImageField(upload_to='profile_pictures/', blank=True,null=True)
    first_name=models.CharField(max_length=30,blank=True,null=True)
    last_name =models.CharField(max_length=30,blank=True,null=True)
    education=models.CharField(max_length=100,blank=True, null=True)
    gender=models.CharField(max_length=15,blank=True,null=True)
    date_of_birth =models.DateField(blank=True,null=True)
    about=models.TextField()  

    job = models.CharField(max_length=50,blank=True,null=True)
    country=models.CharField(max_length=50,blank=True,null=True)
    skills= models.CharField(max_length=255, blank=True,null=True)
    x =models.URLField(max_length=255,blank=True,null=True) 
    insta =models.URLField(max_length=255,blank=True,null=True)  

    facebook=models.URLField(max_length=255,blank=True,null=True)
    linkedin =models.URLField(max_length=255,blank=True,null=True)

    def __str__(self):
        return self.user.email




# model of jobseeker_Profile
class Skill(models.Model):
    name = models.CharField(max_length =50, null=True, default='')

    def __str__(self):
        return self.name  


class jobseeker_Profile(models.Model):
    user =models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=15,blank=True,null=True)
    address=models.CharField(max_length=255,blank=True,null=True)
    profile_picture=models.ImageField(upload_to='profile_pictures/',blank=True,null=True)
    first_name=models.CharField(max_length=30,blank=True,null=True)
    last_name=models.CharField(max_length=30,blank=True,null=True)
    date_of_birth=models.DateField(blank=True,null=True) 
    about=models.TextField()  
    gender=models.CharField(max_length=15,blank=True,null=True)
    education = models.CharField(max_length=100, blank=True, null=True)
    job=models.CharField(max_length=50,blank=True,null=True)
    country=models.CharField(max_length=50,blank=True,null=True)
    skills = models.ManyToManyField(Skill)
    x =models.URLField(max_length=255,blank=True,null=True)  
    insta =models.URLField(max_length=255,blank=True,null=True)  
    facebook=models.URLField(max_length=255,blank=True,null=True)
    linkedin=models.URLField(max_length=255,blank=True,null=True)

    def __str__(self):
        return self.user.email
