# policy_premium/admin.py
from django.contrib import admin
from django import forms
from .models import MemberToInsure, PaymentInterval, Policy

class PolicyAdminForm(forms.ModelForm):
    class Meta:
        model = Policy
        fields = '__all__'
        widgets = {
            'eligible_members': forms.CheckboxSelectMultiple,
        }

@admin.register(MemberToInsure)
class MemberToInsureAdmin(admin.ModelAdmin):
    list_display = ['eligible_members']

@admin.register(PaymentInterval)
class PaymentIntervalAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    form = PolicyAdminForm
    list_display = ['policy_name', 'description', 'coverage_details', 'premium_amount', 'payment_interval']
    filter_horizontal = ['eligible_members']
