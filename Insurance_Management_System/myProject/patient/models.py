from django.db import models

# Create your models here.
GENDER_CHOICES=[
    ('M','MALE'),
    ('F','FEMALE'),
    ('O','OTHERS')
]

class Patient(models.Model):
    patient_id=models.IntegerField(primary_key=True)
    first_name=models.CharField("Patient's First Name",max_length=30)
    last_name=models.CharField("Patient's Last Name",max_length=30,null=True,blank=True)
    slug=models.SlugField(max_length=30)
    age=models.PositiveIntegerField()
    gender=models.CharField(choices=GENDER_CHOICES,max_length=10)
    dateofbirth=models.DateField()
    mobile_number=models.CharField("Patient's Mobile Number",max_length=10)
    email=models.EmailField()
    address=models.TextField()
    profileimage=models.ImageField(upload_to="images/patient/")

    def __str__(self):
        return self.first_name + " "+ self.last_name