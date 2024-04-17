# policy_premium/urls.py
from django.urls import path
from .views import PolicyListView, ViewPolicy, HealthDetails, PersonalDetails, PaymentView

urlpatterns = [
    path('policy_list/', PolicyListView.as_view(), name='policy_list'),
    path('view_policy/', ViewPolicy.as_view(), name='view_policy'),
    path('health_details/', HealthDetails.as_view(), name='health_details'),
    path('personal_details/', PersonalDetails.as_view(), name='personal_details'),
    path('payment/', PaymentView.as_view(), name='payment'),
]
