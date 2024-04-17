from django.shortcuts import render
from .models import Patient

# Create your views here.

def  getAllPatients(request):
    all_patients=Patient.objects.all()
    context={
        'all_patients_key':all_patients
    }
    return render(request,'patient/all_patient.html',context)
