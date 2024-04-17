from django.shortcuts import render
from .models import Hospital
from django.views.decorators.cache import never_cache
#Create your views here.


def getHospitals(request):
    # Fetch data from the User and Hospital models
    all_hospitals = Hospital.objects.all()
    all_users = User.objects.all()

    context = {
        'all_hospitals': all_hospitals,
        'all_users': all_users,
    }

    return render(request, 'hospitals.html', context)

# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required


# # ... other imports ...

# @login_required
# def getHospitals(request):
#     if request.method == "POST":
#         hospital_id = request.POST.get('hospital_id')
#         action = request.POST.get('action')

#         try:
#             hospital = Hospital.objects.get(hospital_id=hospital_id)

#             if action == 'approve':
#                 hospital.approval_status = 'A'
#                 send_mail_to_hospital(hospital, 'approved')
#             elif action == 'reject':
#                 hospital.approval_status = 'R'
#                 send_mail_to_hospital(hospital, 'rejected')
#             elif action == 'activate':
#                 hospital.approval_status = 'A'
#                 send_mail_to_hospital(hospital, 'activated')
#             elif action == 'deactivate':
#                 hospital.approval_status = 'D'
#                 send_mail_to_hospital(hospital, 'deactivated')
#             else:
#                 return JsonResponse({'error': 'Invalid action.'}, status=400)

#             hospital.save()
#             return JsonResponse({'success': True})

#         except Hospital.DoesNotExist:
#             return JsonResponse({'error': 'Hospital not found.'}, status=404)

#     hospitals = Hospital.objects.all()
#     context = {
#         'all_hospitals': hospitals,
#     }

#     return render(request, 'hospitals.html', context)

def send_mail_to_hospital(hospital, status):
    subject = f'Your Hospital Registration has been {status}'
    message = render_to_string('email/hospital_notification.html', {'hospital': hospital, 'status': status})
    from_email = 'your_admin_email@example.com'  # Update with your admin email
    to_email = [hospital.user.email]
    send_mail(subject, message, from_email, to_email, fail_silently=False)


from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Hospital
from .models import User  # Alias to differentiate from Django's User model
from django.conf import settings  # Import Django settings
from django.http import HttpResponse


def hospital_registration(request):
    if request.method == "POST":
        # Extract data from the form
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        category = request.POST.get('category')
        #category="private"
        name = request.POST.get('name')
        address = request.POST.get('address')
        logo = request.FILES.get('logo')
        #print(email,phone,name,address,"DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")


        if password != confirm_password:
            messages.warning(request, "Passwords do not match")
           
            return render(request, 'hospital/hospital_registration.html')

        try:
            if User.objects.filter(email=email).exists():
                messages.warning(request, "Email is already taken")
                
                return render(request, 'hospital/hospital_registration.html')
        except User.DoesNotExist:
            pass

        # Create a User instance for the hospital
        user = User.objects.create_user(email=email, password=password, username=email, role='HOSPITAL')
        
        # Create a Hospital instance and link it to the User
        hospital = Hospital(category=category, name=name, address=address, logo=logo, phone=phone)
        hospital.user = user
        hospital.save()

        # current_site = get_current_site(request)
        # email_subject = "Activate your hospital account"
        # message = render_to_string('activate_hospital.html', {
        #     'user': user,
        #     'domain': current_site.domain,
        #     'uid' : urlsafe_base64_encode(str(user.pk).encode()),

        #     'token': default_token_generator.make_token(user)
        # })

        # email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])
        # email_message.send()

        # messages.info(request, "Activate your hospital account by clicking the link sent to your email")
        return redirect('/handlelogin')  # Redirect to login or success page

    return render(request, 'hospital/hospital_registration.html')




from django.shortcuts import render, redirect
from .models import Hospital
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def hospital_updation(request):
    user = request.user

    try:
        hospital = Hospital.objects.get(user=user)
    except Hospital.DoesNotExist:
        hospital = Hospital(user=user)

    if request.method == 'POST':
        category = request.POST.get('category')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        hospital.category = category
        hospital.name = name
        hospital.phone = phone
        hospital.address = address
        

        if 'logo' in request.FILES:
            hospital.logo = request.FILES['logo']
        # if 'logo' in request.FILES:
        #     hospital.logo = request.FILES['logo']
        #     print("Logo Name:", hospital.logo.name)  # Add this line to print the logo name


        hospital.save()
        messages.success(request, 'Profile updated successfully.')

    return render(request, 'hospital/hospital_updation.html', {'hospital': hospital})




from django.shortcuts import render
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from patient.models import Patient
from PIL import Image

# ... other imports ...

def generate_pdf(request, patient_id):
    try:
        each_patient = Patient.objects.get(patient_id=patient_id)
    except Patient.DoesNotExist:
        return HttpResponse("Patient not found")

    # Create a PDF document
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Add patient details to the PDF
    p.drawString(100, 800, f'Patient ID: {each_patient.patient_id}')
    p.drawString(100, 780, f'Patient\'s Full Name: {each_patient.first_name} {each_patient.last_name}')
    p.drawString(100, 760, f'DOB: {each_patient.dateofbirth}')
    p.drawString(100, 740, f'Gender: {each_patient.gender}')
    p.drawString(100, 720, f'Email: {each_patient.email}')
    p.drawString(100, 700, f'Mobile: {each_patient.mobile_number}')
    p.drawString(100, 680, f'Address: {each_patient.address}')
    # Add more details as needed
    #  # Include the logo in the PDF
    # if each_patient.hospital.logo:
    #     logo_path = each_patient.hospital.logo.path
    #     p.drawInlineImage(logo_path, 400, 750, width=100, height=100)
    # Add the profile image to the PDF if it exists
    if each_patient.profileimage:
        profile_image_path = each_patient.profileimage.path
        profile_image = Image.open(profile_image_path)
        profile_image = profile_image.resize((100, 100))  # Resize the image if needed
        p.drawInlineImage(profile_image_path, 400, 750, width=100, height=100)

    p.save()

    # Move the buffer's pointer to the beginning
    buffer.seek(0)

    # Create an HttpResponse object with the PDF data
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=Patient_{patient_id}_Details.pdf'

    buffer.close()

    return response

# ... other views ...
