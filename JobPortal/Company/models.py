from django.db import models

from UserApplicant.models import User

class Company(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100,blank=True,null=True)
    # start_date=models.PositiveIntegerField(blank=True,null=True)
    start_date=models.DateField(blank=True, null=True)
    country=models.CharField(max_length=255,blank=True,null=True)
    state=models.CharField(max_length=100,blank=True,null=True)
    city=models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return str(self.name)

