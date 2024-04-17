from django.db import models
from datetime import datetime
from home.models import *


# Create your models here.

# class Hospital_Type(models.Model):
#     type_name=models.CharField(max_length=50)
#     slug=models.SlugField(max_length=50)

#   # converts the objects into readablr formats (string)
#     def __str__(self):
#         return self.type_name
  

class Hospital(models.Model):
    # APPROVAL_CHOICES = [
    #     ('P', 'Pending'),
    #     ('A', 'Approved'),
    #     ('R', 'Rejected'),
    # ]

    # ACTIVATION_CHOICES = [
    #     ('A', 'Activated'),
    #     ('D', 'Deactivated'),
    # ]
    hospital_id=models.IntegerField(primary_key=True)
    #loginFkey=models.ForeignKey(User,on_delete=models.CASCADE)
    #category=models.ForeignKey(Hospital_Type,on_delete=models.CASCADE)
    category=models.CharField(max_length=10)
    name=models.CharField(max_length=50)
    slug=models.SlugField(max_length=50)
    #email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, unique=True)
    address=models.TextField()
    updated_date=models.DateTimeField(default=datetime.now)
    logo=models.ImageField(
        upload_to="images/hospital/",blank=True,null=True
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #approval_status = models.CharField(max_length=1, choices=APPROVAL_CHOICES, default='P')
    #activation_status = models.CharField(max_length=1, choices=ACTIVATION_CHOICES, default='D')

      # converts the objects into readablr formats (string)
    def __str__(self):
        return self.name
    
   