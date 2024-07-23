
from django.db import models
from UserApplicant.models import User

class Resume(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=255,blank=True,null=True)
    resume =models.FileField(upload_to='resumes/',max_length=255,blank=True,null=True)
    cover_letter=models.FileField(upload_to='cover_letters/',max_length=255,blank=True,null=True)
    def __str__(self):
        return f"{self.title}"
