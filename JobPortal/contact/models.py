from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField(max_length=40)
    subject = models.CharField(max_length=400)
    message = models.TextField()
   
    def __str__(self):
        return f'{self.name} - {self.subject}'
