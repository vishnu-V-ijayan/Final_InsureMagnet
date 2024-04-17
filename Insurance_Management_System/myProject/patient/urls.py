from django.urls import path
from . import views

urlpatterns = [

# 3 parameters required -- path_name--view_name--url_name...!

path('allpatients/',views.getAllPatients,name="patients"),

]
