# policy_premium/views.py
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from policy_premium.models import MemberToInsure, HealthDetails, SelectedDisease, Policy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class PolicyListView(View):
    template_name = 'policy_premium/policy_list.html'

    def get(self, request, *args, **kwargs):
        policies = Policy.objects.all()
        return render(request, self.template_name, {'policies': policies})

    def post(self, request, *args, **kwargs):
        # Implement logic to handle form submission
        # Retrieve data from the session if needed
        selected_members = request.session.get('selected_members', [])
        pre_existing_diseases = request.session.get('pre_existing_diseases', None)
        pincode = request.session.get('pincode', None)

        # Implement further logic as needed
        #messages.success(request, 'Policy details saved successfully!')

        #return HttpResponse("Policy details saved successfully!")
        
        if pre_existing_diseases == 'on':
            # If pre-existing diseases checkbox is checked, redirect to health_details
            return redirect('health_details')
        else:
            # If not checked, redirect to policy_list
            return redirect('policy_list')


class ViewPolicy(View):
    template_name = 'policy_premium/view_policies.html'

    def get(self, request, *args, **kwargs):
        # Implement any necessary logic
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        pre_existing_diseases = request.POST.get('preExistingDiseases')
        pincode = request.POST.get('pincode')

        # Store data in the session
        request.session['pre_existing_diseases'] = pre_existing_diseases
        request.session['pincode'] = pincode

        if pre_existing_diseases == 'on':
            # If pre-existing diseases checkbox is checked, redirect to health_details
            return redirect('health_details')
        else:
            # If not checked, redirect to policy_list
            return redirect('policy_list')


class HealthDetails(View):
    template_name = 'policy_premium/health_details.html'

    def get(self, request, *args, **kwargs):
        # Implement any necessary logic
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Implement logic to handle form submission
        # Store data in the session if needed
        return HttpResponse("Health details saved successfully!")


class PersonalDetails(View):
    template_name = 'policy_premium/personal_details.html'

    def get(self, request, *args, **kwargs):
        # Implement any necessary logic
        return render(request, self.template_name)


class PaymentView(View):
    template_name = 'policy_premium/payment.html'

    def get(self, request, *args, **kwargs):
        # Implement any necessary logic
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Implement logic to handle form submission
        return HttpResponse("Payment successful!")

# Add your other views as needed
