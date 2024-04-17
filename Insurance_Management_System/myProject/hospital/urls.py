from django.urls import path
from . import views
from .views import generate_pdf 


urlpatterns = [

# 3 parameters required -- path_name--view_name--url_name...!

path('hospitalsdata/',views.getHospitals,name='allhospitals'),
path('hospital_registration/', views.hospital_registration, name='hospital_registration'),
path('hospital_updation/',views.hospital_updation,name="hospital_updation"),
# path('hospital/update/<int:hospital_id>/',views.hospital_update, name='hospital_update'),
path('generate_pdf/<int:patient_id>/', views.generate_pdf, name='generate_pdf'),
path('generate_pdf/<int:patient_id>/', generate_pdf, name='generate_pdf'),






]
