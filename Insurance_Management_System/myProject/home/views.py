import email

from django.forms import PasswordInput
from home import *;
from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .models import User


from django.contrib.auth import authenticate, login,logout
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from patient.models import Patient
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import User
from django.contrib.auth import authenticate, login,logout
from django.utils.encoding import DjangoUnicodeDecodeError
from . import forms,models
from . import models as CMODEL
from .models import *
from .models import PolicyRecord
from . import forms as CFORM
from django.views.generic import View
from .utils import *
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.validators import validate_image_file_extension
#for activating user account
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from home.models import Customer, Policy, PolicyRecord, Category, Question
#email
from django.conf import settings
from django.core.mail import EmailMessage
#threading
import threading
#reset passwor generater
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from .models import Customer
from django.contrib.auth.hashers import make_password
from django.conf import settings

class EmailThread(threading.Thread):
       def __init__(self, email_message):
              super().__init__()
              self.email_message=email_message
       def run(self):
              self.email_message.send()
# Create your views here.

@never_cache

def index(request):
    return render(request, 'index.html')
    #return HttpResponse("Hello World..!")
User = get_user_model()

def Sign_up(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.warning(request, "Password is not matching")
            return render(request, 'signup.html')

        try:
            # Check if the email is already taken
            if User.objects.get(username=email):
                messages.warning(request, "Email is already taken")
                return render(request, 'signup.html')
        except User.DoesNotExist:
            pass

        # Create a user with email and password
        user = User.objects.create_user(email=email, password=password, username=email, role='CUSTOMER')
        user.is_active = False
        user.save()

        # Create a Customer instance with additional details
        customer = Customer.objects.create(
            user=user,
            first_name=request.POST['fname'],
            last_name=request.POST['lname'],
            phone=request.POST['phone'],
            aadhaar=request.POST['aadhaar_number'],
            address=request.POST['address'],
            # Add other fields as needed
        )
        
        # Handle image field separately if it's included in the form
        if 'profile_picture' in request.FILES:
            profile_picture = request.FILES['profile_picture']
            try:
                # Validate the image file extension
                validate_image_file_extension(profile_picture)
            except ValidationError as e:
                messages.warning(request, f"Invalid image file: {e}")
                return render(request, 'signup.html')

            customer.image = profile_picture

        # # Handle image field separately if it's included in the form
        # if 'image' in request.FILES:
        #     customer.image = request.FILES['image']

        customer.save()

        # Send activation email
        current_site = get_current_site(request)
        email_subject = "Activate your account"
        message = render_to_string('activate.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user)
        })

        email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])
        email_message.send()

        messages.info(request, "Activate your account by clicking the link sent to your email")
        return redirect('/handlelogin')

    return render(request, 'signup.html')

class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.info(request,"Account activated sucessfully")
            return redirect('/handlelogin')
        user.is_active=True
        user.save()
        return redirect('/handlelogin')
        #return render(request,"activatefail.html")

def handlelogin(request):
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']
        myuser = authenticate(request, username=username, password=password)
        print(myuser)
        if myuser is not None:
            login(request, myuser)
            request.session['username'] = username

            if myuser.role == 'CUSTOMER':
                #return redirect('customer_dashboard_view')
                return redirect('customer_dashboard')
            elif myuser.role == 'SELLER':
                return HttpResponse("seller login")
            elif myuser.role == 'ADMIN':
                return redirect('/admin_dashboard/')  # Redirect to the admin dashboard page
            elif myuser.role == 'HOSPITAL':
                return redirect('/hospital_dashboard/')
            elif myuser.role == 'STAFF':
                return redirect('staffhome')
            elif myuser.role == 'AGENT':
                return redirect('agenthome')


        else:
            messages.error(request, "Enter valid credentials")
            return redirect('/handlelogin')
    
    response = render(request, 'login.html')
    response['Cache-Control'] = 'no-store, must-revalidate'
    return response

@never_cache
@login_required(login_url='/handlelogin/')
def customer_home(request):
       if 'username' in request.session:
        response = render(request,'customer_page.html')
        response['Cache-Control'] = 'no-store,must-revalidate'
        return response
       else:
             return redirect('handlelogin')

def handlelogout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')

@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    dict={
        'total_user':Customer.objects.all().count(),
        'total_policy':Policy.objects.all().count(),
        'total_category':Category.objects.all().count(),
        'total_question':Question.objects.all().count(),
        'total_policy_holder':PolicyRecord.objects.all().count(),
        'approved_policy_holder':PolicyRecord.objects.all().filter(status='Approved').count(),
        'disapproved_policy_holder':PolicyRecord.objects.all().filter(status='Disapproved').count(),
        'waiting_policy_holder':PolicyRecord.objects.all().filter(status='Pending').count(),
    }
    return render(request,'dashboard.html',context=dict)

#################################################################################################
#################################################################################################
#################################################################################################

#@login_required(login_url='adminlogin')
def admin_view_customer_view(request):
    # Fetch data from the User and Customer models
    all_customers = Customer.objects.all()
    #all_users = User.objects.all()


    return render(request, 'admin/admin_view_customer.html', {'all_customers': all_customers})

@login_required(login_url='adminlogin')
def update_customer_view(request,pk):
    customer=CMODEL.Customer.objects.get(id=pk)
    user=CMODEL.User.objects.get(id=customer.user_id)
    userForm=CFORM.CustomerUserForm(instance=user)
    customerForm=CFORM.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=CFORM.CustomerUserForm(request.POST,instance=user)
        customerForm=CFORM.CustomerForm(request.POST,request.FILES,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('admin-view-customer')
    return render(request,'admin/update_customer.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_customer_view(request,pk):
    customer=CMODEL.Customer.objects.get(id=pk)
    user=User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return HttpResponseRedirect('/admin-view-customer')



def admin_category_view(request):
    return render(request,'admin/admin_category.html')

def admin_add_category_view(request):
    categoryForm=forms.CategoryForm() 
    if request.method=='POST':
        categoryForm=forms.CategoryForm(request.POST)
        if categoryForm.is_valid():
            categoryForm.save()
            return redirect('admin-view-category')
    return render(request,'admin/admin_add_category.html',{'categoryForm':categoryForm})

def admin_view_category_view(request):
    categories = Category.objects.all()
    return render(request,'admin/admin_view_category.html',{'categories':categories})

def admin_delete_category_view(request):
    categories = Category.objects.all()
    return render(request,'admin/admin_delete_category.html',{'categories':categories})
    
def delete_category_view(request,pk):
    category = Category.objects.get(id=pk)
    category.delete()
    return redirect('admin-delete-category')

def admin_update_category_view(request):
    categories = Category.objects.all()
    return render(request,'admin/admin_update_category.html',{'categories':categories})

@login_required(login_url='adminlogin')
def update_category_view(request,pk):
    category = Category.objects.get(id=pk)
    categoryForm=forms.CategoryForm(instance=category)
    
    if request.method=='POST':
        categoryForm=forms.CategoryForm(request.POST,instance=category)
        
        if categoryForm.is_valid():

            categoryForm.save()
            return redirect('admin-update-category')
    return render(request,'admin/update_category.html',{'categoryForm':categoryForm})
  
def admin_policy_view(request):
    return render(request,'admin/admin_policy.html')


def admin_add_policy_view(request):
    policyForm=forms.PolicyForm() 
    
    if request.method=='POST':
        policyForm=forms.PolicyForm(request.POST)
        if policyForm.is_valid():
            categoryid = request.POST.get('category')
            category = Category.objects.get(id=categoryid)
            
            policy = policyForm.save(commit=False)
            policy.category=category
            policy.save()
            return redirect('admin-view-policy')
    return render(request,'admin/admin_add_policy.html',{'policyForm':policyForm})

def admin_view_policy_view(request):
    policies = Policy.objects.all()
    return render(request,'admin/admin_view_policy.html',{'policies':policies})

def admin_update_policy_view(request):
    policies = Policy.objects.all()
    return render(request,'admin/admin_update_policy.html',{'policies':policies})

@login_required(login_url='adminlogin')
def update_policy_view(request,pk):
    policy = Policy.objects.get(id=pk)
    policyForm=forms.PolicyForm(instance=policy)
    
    if request.method=='POST':
        policyForm=forms.PolicyForm(request.POST,instance=policy)
        
        if policyForm.is_valid():

            categoryid = request.POST.get('category')
            category = Category.objects.get(id=categoryid)
            
            policy = policyForm.save(commit=False)
            policy.category=category
            policy.save()
           
            return redirect('admin-update-policy')
    return render(request,'admin/update_policy.html',{'policyForm':policyForm})
  
  
def admin_delete_policy_view(request):
    policies = Policy.objects.all()
    return render(request,'admin/admin_delete_policy.html',{'policies':policies})
    
def delete_policy_view(request,pk):
    policy = Policy.objects.get(id=pk)
    policy.delete()
    return redirect('admin-delete-policy')

###

def admin_view_policy_holder_view(request):
    policyrecords = PolicyRecord.objects.all()
    return render(request,'admin/admin_view_policy_holder.html',{'policyrecords':policyrecords})

def admin_view_approved_policy_holder_view(request):
    policyrecords = PolicyRecord.objects.all().filter(status='Approved')
    return render(request,'admin/admin_view_approved_policy_holder.html',{'policyrecords':policyrecords})

def admin_view_disapproved_policy_holder_view(request):
    policyrecords = PolicyRecord.objects.all().filter(status='Disapproved')
    return render(request,'admin/admin_view_disapproved_policy_holder.html',{'policyrecords':policyrecords})

def admin_view_waiting_policy_holder_view(request):
    policyrecords = PolicyRecord.objects.all().filter(status='Pending')
    return render(request,'admin/admin_view_waiting_policy_holder.html',{'policyrecords':policyrecords})

def approve_request_view(request,pk):
    policyrecords = PolicyRecord.objects.get(id=pk)
    policyrecords.status='Approved'
    policyrecords.save()
    return redirect('admin-view-policy-holder')

def disapprove_request_view(request,pk):
    policyrecords = PolicyRecord.objects.get(id=pk)
    policyrecords.status='Disapproved'
    policyrecords.save()
    return redirect('admin-view-policy-holder')


def admin_question_view(request):
    questions = Question.objects.all()
    return render(request,'admin/admin_question.html',{'questions':questions})

def update_question_view(request,pk):
    question = Question.objects.get(id=pk)
    questionForm=forms.QuestionForm(instance=question)
    
    if request.method=='POST':
        questionForm=forms.QuestionForm(request.POST,instance=question)
        
        if questionForm.is_valid():

            admin_comment = request.POST.get('admin_comment')
            
            
            question = questionForm.save(commit=False)
            question.admin_comment=admin_comment
            question.save()
           
            return redirect('admin-question')
    return render(request,'admin/update_question.html',{'questionForm':questionForm})

##################################################################################################
##################################################################################################
##################################################################################################


@never_cache
@login_required(login_url='/handlelogin/')
def hospital_dashboard(request):
      patients=Patient.objects.all()

      return render(request,"hospital/hospital_dashboard.html",{'patients': patients})


def customer_dashboard(request):
    customer = get_object_or_404(Customer, user=request.user)
    

    available_policy_count = Policy.objects.all().count()
    applied_policy_count = PolicyRecord.objects.filter(customer=customer).count()
    total_category_count = Category.objects.all().count()
    total_question_count = Question.objects.filter(customer=customer).count()

    context = {
        'customer': customer,
        'available_policy': available_policy_count,
        'applied_policy': applied_policy_count,
        'total_category': total_category_count,
        'total_question': total_question_count,
    }

    return render(request, 'customer/customer_dashboard.html', context)

# def apply_policy_view(request):
#     customer = get_object_or_404(models.Customer,user_id=request.user.id)
#     policies = CMODEL.Policy.objects.all()
#     return render(request,'customer/apply_policy.html',{'policies':policies,'customer':customer})

from django.shortcuts import render, get_object_or_404
import razorpay
from . import models as CMODEL  # Assuming your models are in models.py within the same app

# Initialize Razorpay client

def apply_policy_view(request):
    customer = get_object_or_404(CMODEL.Customer, user_id=request.user.id)
    policies = CMODEL.Policy.objects.all()

    # Fixed amount for Razorpay payment, for demonstration
    

    # Context for rendering in the template
    context = {
        
        'policies': policies,
        'customer': customer
    }

    # Use the 'apply_policy.html' template or another template that includes the Razorpay JavaScript code
    return render(request, 'customer/apply_policy.html', context=context)

import razorpay
from django.shortcuts import render
from django.conf import settings

razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

# views.py

def payment2(request, item_id):
    
    currency = 'INR'
    amount = 2000 * 100  # Rs. 2000, converted to paise

    # You can use item_id here, for example, to get data related to what is being paid for
    # item = get_object_or_404(MyModel, id=item_id)  # Assuming you're paying for items stored in a model

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='1'))

    razorpay_order_id = razorpay_order['id']
    callback_url = 'your_callback_url_here'  # Specify your callback URL here

    context = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,
        'currency': currency,
        'callback_url': callback_url,
        # 'item': item,  # You can pass the item to the template, if necessary
    }
    return render(request, 'customer/payment2.html', context=context)








def apply_view(request,pk):
    customer = models.Customer.objects.get(user_id=request.user.id)
    policy = CMODEL.Policy.objects.get(id=pk)
    policyrecord = CMODEL.PolicyRecord()
    policyrecord.Policy = policy
    policyrecord.customer = customer
    policyrecord.save()
    return redirect('history')

def history_view(request):
    customer = Customer.objects.get(user_id=request.user.id)
    policies = CMODEL.PolicyRecord.objects.all().filter(customer=customer)
    return render(request,'customer/history.html',{'policies':policies,'customer':customer})

def ask_question_view(request):
    customer = Customer.objects.get(user_id=request.user.id)
    questionForm=CFORM.QuestionForm() 
    
    if request.method=='POST':
        questionForm=CFORM.QuestionForm(request.POST)
        if questionForm.is_valid():
            
            question = questionForm.save(commit=False)
            question.customer=customer
            question.save()
            return redirect('question-history')
    return render(request,'customer/ask_question.html',{'questionForm':questionForm,'customer':customer})

def question_history_view(request):
    customer = Customer.objects.get(user_id=request.user.id)
    questions = CMODEL.Question.objects.all().filter(customer=customer)
    return render(request,'customer/question_history.html',{'questions':questions,'customer':customer})



"""def employee_signup(request):
    if request.method == 'POST':
        # Handle User registration (username and password)
        email = request.POST['email']
        password = request.POST['password']

        # Set the username to the user's email
        username = email

        # Create a User instance
        user = User.objects.create_user(username=username, email=email, password=password)

        # Handle EmployeeRegistration
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        address = request.POST['address']
        resume_upload = request.FILES['resume_upload']

        # Create an EmployeeRegistration instance
        employee_registration = EmployeeRegistration(
            user=user,  # Link the User to the EmployeeRegistration
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            resume_upload=resume_upload
        )
        employee_registration.save()

        # Redirect to a success page or do other necessary actions
        return redirect('index')  # Change 'success_page' to the URL for the success page

    # Handle form errors and render the registration form
    return render(request, 'employee_signup.html')"""

   

# def Sign_up(request):
#     if request.method=="POST":
#             fname=request.POST['fname']
#             lname=request.POST['lname']
#             email=request.POST['email']
#             #phone=request.POST['phone']
#             username=email
            
#             password=request.POST['password']
#             confirm_password=request.POST['confirm_password']


            
#             if password!=confirm_password:
#                     messages.warning(request,"password is not matching")
#                     return render(request,'signup.html')
#             try:
#                       if User.objects.get(username=email):
#                              messages.warning(request,"Email is already taken")
#                              return render(request,'signup.html')
#             except Exception as identifiers:
#                       pass

#             user=User.objects.create_user(first_name=fname,last_name=lname,email=email,password=password,username=username,role='CUSTOMER')
#             user.is_active=False 
#             user.save()
#             current_site=get_current_site(request)  
#             email_subject="Activate your account"
#             message=render_to_string('activate.html',{
#                    'user':user,
#                    'domain':current_site.domain,
#                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#                    'token':generate_token.make_token(user)


#             })

#             email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
#             EmailThread(email_message).start()
#             messages.info(request,"Active your account by clicking the link send to your email")



           
#             return redirect('/handlelogin')
           
             
           
#     return render(request,'signup.html')


# def customer_dashboard(request):
#     # dict={
#     #     'customer':get_object_or_404(models.Customer,user_id=request.user.id),
#     #     'available_policy':CMODEL.Policy.objects.all().count(),
#     #     'applied_policy':CMODEL.PolicyRecord.objects.all().filter(customer=models.Customer.objects.get(user_id=request.user.id)).count(),
#     #     'total_category':CMODEL.Category.objects.all().count(),
#     #     'total_question':CMODEL.Question.objects.all().filter(customer=models.Customer.objects.get(user_id=request.user.id)).count(),

#     # }
#     return render(request,'customer/customer_dashboard.html')





from .forms import CustomerSelectForm
from .models import *

def select_customer(request):
    if request.method == 'POST':
        form = CustomerSelectForm(request.POST)
        if form.is_valid():
            customer_id = form.cleaned_data['customer'].id
            return redirect('customer_details', customer_id=customer_id)
    else:
        form = CustomerSelectForm()
    return render(request, 'select_customer.html', {'form': form})

def customer_details(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    return render(request, 'customer_details.html', {'customer': customer})

def customer_details(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    plans = VehiclePlan.objects.all()
    return render(request, 'customer_details.html', { 'customer': customer,'plans': plans})

def staff_view_policy_holder_view(request):
    policyrecords = PolicyRecord.objects.all()
    return render(request,'staff/staff-view-policy-holder.html',{'policyrecords':policyrecords})


def staff_view_approved_policy_holder_view(request):
    policyrecords = PolicyRecord.objects.all().filter(status='Approved')
    return render(request,'staff/staff_view_approved_policy_holder.html',{'policyrecords':policyrecords})

def staff_view_disapproved_policy_holder_view(request):
    policyrecords = PolicyRecord.objects.all().filter(status='Disapproved')
    return render(request,'staff/staff_view_disapproved_policy_holder.html',{'policyrecords':policyrecords})

def staff_view_waiting_policy_holder_view(request):
    policyrecords = PolicyRecord.objects.all().filter(status='Pending')
    return render(request,'staff/staff_view_waiting_policy_holder.html',{'policyrecords':policyrecords})

def staff_approve_request_view(request,pk):
    policyrecords = PolicyRecord.objects.get(id=pk)
    policyrecords.status='Approved'
    policyrecords.save()
    return redirect('staff-view-policy-holder')

def staff_disapprove_request_view(request,pk):
    policyrecords = PolicyRecord.objects.get(id=pk)
    policyrecords.status='Disapproved'
    policyrecords.save()
    return redirect('staff-view-policy-holder')



# from django.shortcuts import render, redirect
# from django.utils import timezone
# from .models import Office
# from django.contrib.auth.models import User

# def office_registration(request):
#     if request.method == "POST":
#         # Process form data
#         address = request.POST.get('address')
#         place = request.POST.get('place')
#         location = request.POST.get('location')
#         pin = request.POST.get('pin')
#         phone = request.POST.get('phone')
#         district = request.POST.get('district')
#         state = request.POST.get('state')
#         regdate = timezone.now().date()  # Capture current date for registration
        
#         # Create and save new Office instance
#         office = Office.objects.create(
#             address=address, place=place, location=location,
#             pin=pin, phone=phone, district=district, state=state, regdate=regdate
#         )

#         # Assuming you want to register a user when an office is registered
#         # Note: Make sure the user registration logic is relevant and secure
#         user = User.objects.create_user(username=place, password='default_password', is_active=False)
#         user.save()

#         # Redirect to a success page or back to form with a success message
#         return redirect('admin/admin_office_registration_successfull.html')  # Replace 'success_page_url' with your actual URL
#     else:
#         # GET request, show empty form
#         return render(request, 'admin_office_registration.html')

    

def staff_home(request):
    return render(request,'staff_home.html')




from django.conf import settings

from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from .models import Agent,Staff

@never_cache
def add_agent(request):
    if request.method == 'POST':
        # User model fields
        email = request.POST['email']
        name = request.POST['name']

        # Generate a random password
        password = get_random_string(length=8)

        # Create User instance
        user = User.objects.create_user(username=email, email=email, password=password, first_name=name,role=User.Role.AGENT)
        user.save()

        # Agent model fields
        agent = Agent(
            user=user,
            name=name,
            address=request.POST['address'],
            place=request.POST['place'],
            location=request.POST['location'],
            pin=request.POST['pin'],
            phone=request.POST['phone'],
            gender=request.POST['gender'],
            qualification=request.POST['qualification'],
            aadhar=request.POST['aadhar'],
            registration_date=request.POST['registration_date'],
            # Assuming request.FILES is properly set up in your form for handling file uploads
            photo=request.FILES.get('photo', None)
        )
        agent.save()

        # Send email to the user
        send_mail(
            'Your Account Information',
            f'Your account has been created. Your password is: {password}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return HttpResponse("agent added sucessfully")  # Redirect to a new URL

    return render(request, 'add_agent.html')

def register_staff(request):
    if request.method == "POST":
        # Extracting information from the request
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        place = request.POST['place']
        pin = request.POST['pin']
        district = request.POST['district']
        state = request.POST['state']
        dob = request.POST['dob']
        photo = request.FILES['photo'] if 'photo' in request.FILES else None
        password = request.POST['password']
        
        # Create user instance
        User = get_user_model()
        user = User.objects.create(
            username=email,  # Assuming username is email for simplicity
            email=email,
            password=make_password(password),
            role=User.Role.STAFF
        )
        # Optionally, you can use user.set_password(password) to handle hashing
        user.save()
        
        # Create staff instance
        staff = Staff(
            user=user,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            place=place,
            pin=pin,
            district=district,
            state=state,
            dob=dob,
            photo=photo
        )
        staff.save()

        # Redirect to a new URL:
        return redirect('staffhome')

    # If a GET (or any other method) we'll create a blank form
    else:
        return render(request, 'register.html')

# Remember to include the appropriate URLconf if you haven't already done so


def agenthome(request):
    return render(request,'agenthome.html')

from .models import Office
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import datetime

from django.urls import reverse
from django.shortcuts import redirect

@csrf_exempt
def register_office(request):
    if request.method == 'POST':
        new_office = Office(
            address=request.POST.get('address'),
            place=request.POST.get('place'),
            location=request.POST.get('location'),
            pin=request.POST.get('pin'),
            phone=request.POST.get('phone'),
            district=request.POST.get('district'),
            state=request.POST.get('state'),
            regdate=datetime.date.today()
        )
        new_office.save()

        # Redirect to the success page, passing the ID of the newly created office
        return redirect(reverse('office_success', kwargs={'office_id': new_office.officeid}))
    else:
        return render(request, 'admin/admin_office_registration.html')

from django.shortcuts import render, get_object_or_404

def office_detail(request, office_id):
    office = get_object_or_404(Office, officeid=office_id)
    return render(request, 'admin/admin_office_detail.html', {'office': office})


# # Assuming you want a view to display the office details
# def office_detail(request, office_id):
#     office = Office.objects.get(id=office_id)
#     return render(request, 'admin/admin_office_detail.html', {'office': office})

def view_office(request):
    var=Office.objects.all()
    context={
        'var':var
    }
    return render(request, 'admin/admin_office_registration_successfull.html', context)

#staff registration

from django.views.decorators.csrf import csrf_exempt
from .models import Office, Staff
from django.conf import settings

@csrf_exempt
def register_staff(request):
    if request.method == 'POST':
        # Extracting form data using more descriptive names
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        place = request.POST.get('place')
        pin = request.POST.get('pin')
        phone = request.POST.get('phone')
        district = request.POST.get('district')
        state = request.POST.get('state')
        dob = request.POST.get('dob')
        photo = request.FILES.get('photo')
        office_id = request.POST.get('office_id')
        designation = request.POST.get('designation')

        # Saving the staff details
        try:
            office = Office.objects.get(pk=office_id)
            staff = Staff(
                user=request.user,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                address=office.address,
                place=place,
                pin=pin,
                district=district,
                state=state,
                dob=dob,
                photo=photo
            )
            staff.save()
            return redirect('admin/admin_staff_registration_successful.html')
        except Exception as e:
            print(e)
            return render(request, 'admin/admin_staff_registration.html', {'error': 'Error while registering the staff'})

    # For GET request, or if there is any other issue
    offices = Office.objects.all()
    return render(request, 'admin/admin_staff_registration.html', {'records': offices})

def list_offices(request):
    offices = Office.objects.all()
    return render(request, 'admin/admin_staff_registration.html', {'records': offices})


def admin_staff_registration_successful(request, staff_id):
    staff = Staff.objects.get(id=staff_id)
    return render(request, 'admin/admin_staff_registration_successful.html', {'staff': staff})

from django.shortcuts import render, redirect
from .models import VehiclePlan
from django.contrib import messages

def vehicle_plan_registration(request):
    if request.method == 'POST':
        p_type = request.POST.get('t1')
        p_percentage = request.POST.get('t2')
        specifications = request.POST.get('t3')
        depreciation = request.POST.get('t4')

        try:
            # Attempt to convert percentage and depreciation to proper formats
            p_percentage = float(p_percentage)
            depreciation = float(depreciation)

            # Create a new VehiclePlan instance and save it
            new_plan = VehiclePlan(PType=p_type, Ppercentage=p_percentage, sp=specifications, depreciation=depreciation)
            new_plan.save()

            # Show success message
            messages.success(request, 'Vehicle plan registered successfully!')
        except ValueError:
            # Handle error if conversion fails
            messages.error(request, 'Invalid input in numeric fields.')
        except Exception as e:
            # General error handling
            messages.error(request, f'Error registering plan: {str(e)}')

    # Load existing plans to display
    records = VehiclePlan.objects.all()
    return render(request, 'admin/admin_vehicleplan_registration.html', {'records': records})

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import HealthPlan
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Remove this if CSRF token works properly; it's just for demonstration.
def health_plan_registration(request):
    if request.method == 'POST':
        # Extract data from the form
        ptype = request.POST.get('t1')
        ypremium = request.POST.get('t2')
        incper = request.POST.get('t3')
        maxamt = request.POST.get('t4')
        specification = request.POST.get('t5')
        uptoage = request.POST.get('t6')
        
        # Create a new HealthPlan object and save it
        try:
            hpid = "HP" + str(HealthPlan.objects.count() + 1)  # Simple example to generate a new ID
            health_plan = HealthPlan(
                hpid=hpid,
                ptype=ptype,
                ypremium=ypremium,
                incper=incper,
                maxamt=maxamt,
                specification=specification,
                uptoage=uptoage
            )
            health_plan.save()
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}")

    # Fetch existing plans to display
    records = HealthPlan.objects.all()
    return render(request, 'admin/admin_healthplan_registration.html', {'records': records})


from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import VehiclePolicy, VehiclePlan, Customer
from decimal import Decimal
import datetime

def register_vehicle_policy(request):
    if request.method == 'POST':
        try:
            # Extract and validate data from form
            vehno = request.POST.get('t2')
            vehvalue = Decimal(request.POST.get('t3', 0))
            vpid = request.POST.get('t4')
            enginno = request.POST.get('t5')
            chno = request.POST.get('t6')
            vehcompany = request.POST.get('t8')
            mfyear = int(request.POST.get('t10', 0))
            vehphoto = request.FILES.get('file')
            vehtype = request.POST.get('t11')
            officeid = request.POST.get('t12')
            custid = request.POST.get('t1')

            # Retrieve related objects
            plan = VehiclePlan.objects.get(id=vpid)
            customer = Customer.objects.get(id=custid)

            # Calculate policy amount
            depreciation_factor = Decimal(plan.depreciation / 100)
            plan_percentage = Decimal(plan.Ppercentage / 100)
            policy_amount = (vehvalue - (vehvalue * depreciation_factor)) * (1 + plan_percentage)

            # Create and save the VehiclePolicy object
            policy = VehiclePolicy(
                custid=customer,
                vehno=vehno,
                vehvalue=vehvalue,
                vpid=plan,
                enginno=enginno,
                chno=chno,
                vehcompany=vehcompany,
                mfyear=mfyear,
                officeid=officeid,
                vehphoto=vehphoto,
                vehtype=vehtype,
                policyamount=policy_amount,
                policydate=datetime.date.today(),
                penddate=datetime.date.today() + datetime.timedelta(days=365)  # assuming policy is valid for one year
            )
            policy.save()

            return redirect('policy_success')  # Redirect to a success URL
        except (VehiclePlan.DoesNotExist, Customer.DoesNotExist, KeyError, ValueError) as e:
            return HttpResponse(f"Error processing your request: {e}", status=400)
    else:
        return render(request, 'customer/customer_vehicle_policyissue.html')

def policy_success(request):
    return render(request, 'customer/customer_vehicle_policyissue_successful.html')





