from django.db import models
from UserApplicant.models import User
from Company.models import Company
from Resume.models import Resume


class Skills_job(models.Model):
    name = models.CharField(max_length=255, blank=True,null=True)

    def __str__(self):
        return self.name

class Education(models.Model):
    name = models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return self.name
    
class SalaryRange(models.Model):
    salary_range = models.CharField(max_length=100)  

    def __str__(self):
        return self.salary_range

class JobPost(models.Model):
    # SALARY_CHOICES = [
    #     ('5,000-10,000' ,'5,000-10,000'),
    #     ('10,000-15,000','10,000-15,000'),
    #     ('15,000-20,000','15,000-20,000'),
    #     ('20,000-25,000','20,000-25,000'),
    #     ('25,000-30,000','25,000-30,000'),
    #     ('30,000-35,000','30,000-35,000'),
    #     ('35,000-40,000','35,000-40,000'),
    #     ('40,000-45,000','40,000-45,000'),
    #     ('45,000-50,000','45,000-50,000'),
    #     ('50,000+','50,000+'),
    # ]

    EXPERIENCE_CHOICES = [
        ('0-1', '0-1 years'),
        ('1-3', '1-3 years'),
        ('3-5', '3-5 years'),
        ('5-10', '5-10 years'),
        ('10+', '10+ years'),
    ]

    JOB_TYPE_CHOICES = [
        ('Full-Time', 'Full-Time'),
        ('Part-Time', 'Part-Time'),
        ('Internship', 'Internship'),
    ]

    user=models.ForeignKey(User, on_delete=models.CASCADE)
    company=models.ForeignKey(Company,on_delete=models.CASCADE,default='Select Your Company')
    skills = models.ManyToManyField(Skills_job, blank=True)
    title=models.CharField(max_length=255,blank=True, null=True)
    education=models.ForeignKey(Education,on_delete=models.CASCADE, default='Highest Qualification')
    salary=models.ForeignKey(SalaryRange,on_delete=models.CASCADE, default='10000-20000')
    overview =models.TextField(max_length=255,blank=True,null=True)
    location=models.CharField(max_length=255,blank=True,null=True)
    job_type =models.CharField(max_length=10,choices=JOB_TYPE_CHOICES,null=True, default='Full-Time')
    experience= models.CharField(max_length=5,choices=EXPERIENCE_CHOICES,null=True)
    # salary =models.CharField(max_length=25,choices=SALARY_CHOICES,default='50+',verbose_name='Salary Range')
    is_active= models.BooleanField(default=False)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return f"{self.title} - {self.company.name}"
    

class Apply_Job(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    job=models.ForeignKey(JobPost,on_delete=models.CASCADE) 
    timestamp=models.DateTimeField(auto_now_add=True)
    status= models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.user.username}-{self.job.title}-{self.status}"
    

class JobApplicationNotification(models.Model):
    Application = models.ForeignKey(Apply_Job,on_delete=models.CASCADE)
    employer = models.ForeignKey(User,related_name="employer_notifications",on_delete=models.CASCADE)
    message = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-time_stamp']

class Message(models.Model):
     sender = models.ForeignKey(User, on_delete=models.CASCADE ,related_name="sender")
     receiver = models.ForeignKey(User,  on_delete=models.CASCADE ,related_name="reciver")
     message = models.TextField()
     timestamp = models.DateTimeField(auto_now_add=True)
     unread = models.BooleanField(default = True)

     