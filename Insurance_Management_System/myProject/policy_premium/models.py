# policy_premium/models.py
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# policy_premium/models.py
import uuid

class MemberToInsure(models.Model):
    SELF = 'Self'
    SPOUSE = 'Spouse'
    SON_DAUGHTER = 'Son/Daughter'
    PARENTS_IN_LAWS = 'Parents/In-laws'

    MEMBER_CHOICES = [
        (SELF, 'Self'),
        (SPOUSE, 'Spouse'),
        (SON_DAUGHTER, 'Son/Daughter'),
        (PARENTS_IN_LAWS, 'Parents/In-laws'),
    ]

    eligible_members = models.CharField(max_length=255, choices=MEMBER_CHOICES, unique=True)

    def __str__(self):
        return self.eligible_members
    
class PaymentInterval(models.Model):
    MONTHLY = 'monthly'
    ANNUALLY = 'annually'

    INTERVAL_CHOICES = [
        (MONTHLY, 'Monthly'),
        (ANNUALLY, 'Annually'),
    ]

    name = models.CharField(max_length=50, choices=INTERVAL_CHOICES, unique=True)

    def __str__(self):
        return self.name


class Policy(models.Model):
    policy_name = models.CharField(max_length=255)
    description = models.TextField()
    coverage_details = models.CharField(max_length=255)
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Add a many-to-many relationship with Member
    eligible_members = models.ManyToManyField(MemberToInsure, blank=True)
    # New field for payment interval
    payment_interval = models.ForeignKey(PaymentInterval, on_delete=models.CASCADE)

    def __str__(self):
        return self.policy_name

class PolicyHolder(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    marital_status = models.CharField(max_length=50, choices=[('single', 'Single'), ('married', 'Married')])
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    current_address = models.TextField()
    pincode = models.CharField(max_length=10)
    nominee_name = models.CharField(max_length=255)
    nominee_relation = models.CharField(max_length=50)
    nominee_date_of_birth = models.DateField()

    def __str__(self):
        return self.user.username
    
class PremiumPlan(models.Model):
    policy = models.ForeignKey('Policy', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.policy.policy_name} - {self.amount} - {self.due_date}"

class InsuredMember(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    policy_holder = models.ForeignKey(PolicyHolder, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        policy_holder_username = self.policy_holder.user.username if self.policy_holder else "No Policy Holder"
        return f"{policy_holder_username} - {self.gender} - {self.date_of_birth}"



class HealthDetails(models.Model):
    DISEASE_CHOICES = [
        ('diabetes', 'Diabetes'),
        ('hypertension', 'Hypertension'),
        ('hiv_aids', 'HIV/AIDS'),
        ('heart_ailments', 'Heart Ailments'),
        ('liver_disease', 'Liver Disease'),
        ('cancer', 'Cancer'),
        ('stroke', 'Stroke'),
    ]
    policy_holder = models.OneToOneField(PolicyHolder, on_delete=models.CASCADE)
    pre_existing_disease = models.BooleanField()
    selected_diseases = models.ManyToManyField('SelectedDisease', blank=True)

class SelectedDisease(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

def generate_transaction_id():
    return uuid.uuid4().hex
class Payment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=255, default=generate_transaction_id)

    def __str__(self):
        return f"{self.policy.policy_name} - {self.user.username}"

