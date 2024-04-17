from django.contrib import admin

# Register your models here.
from .models import User
from .models import *
admin.site.register(User),
admin.site.register(Customer),
admin.site.register(VehiclePlan),
admin.site.register(VehiclePolicy),
admin.site.register(Staff),
admin.site.register(HealthPlan)
admin.site.register(HMembers)
admin.site.register(HealthPolicy)
admin.site.register(Payment)
admin.site.register(ClaimRequest)
admin.site.register(ClaimApproval)
admin.site.register(Office)
