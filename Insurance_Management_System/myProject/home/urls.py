from django.urls import path,include
from . import views

from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
urlpatterns = [
    path('', views.index,name="index"),
    path('signup/',views.Sign_up,name="signup"),
    path('handlelogin/',views.handlelogin,name="handlelogin"),
    path('handlelogout/',views.handlelogout,name="handlelogout"),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),
    path('customer_home/',views.customer_home,name="customer_home"),
    # path('view_policies/',views.view_policies,name="view_policies"),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #path('admin_dashboard/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('admin_dashboard/',views.admin_dashboard_view,name="admin_dashboard"),
    #path('employee_signup/',views.employee_signup,name="employee_signup"),
    path('hospital_dashboard/',views.hospital_dashboard,name="hospital_dashboard"),

   

#############################################################################################

    path('admin-view-customer/', views.admin_view_customer_view, name='admin-view-customer'),
    path('update-customer/<int:pk>', views.update_customer_view,name='update-customer'),
    path('delete-customer/<int:pk>', views.delete_customer_view,name='delete-customer'),

    path('admin-category', views.admin_category_view,name='admin-category'),
    path('admin-view-category', views.admin_view_category_view,name='admin-view-category'),
    path('admin-update-category', views.admin_update_category_view,name='admin-update-category'),
    path('update-category/<int:pk>', views.update_category_view,name='update-category'),
    path('admin-add-category', views.admin_add_category_view,name='admin-add-category'),
    path('admin-delete-category', views.admin_delete_category_view,name='admin-delete-category'),
    path('delete-category/<int:pk>', views.delete_category_view,name='delete-category'),


    path('admin-policy', views.admin_policy_view,name='admin-policy'),
    path('admin-add-policy', views.admin_add_policy_view,name='admin-add-policy'),
    path('admin-view-policy', views.admin_view_policy_view,name='admin-view-policy'),
    path('admin-update-policy', views.admin_update_policy_view,name='admin-update-policy'),
    path('update-policy/<int:pk>', views.update_policy_view,name='update-policy'),
    path('admin-delete-policy', views.admin_delete_policy_view,name='admin-delete-policy'),
    path('delete-policy/<int:pk>', views.delete_policy_view,name='delete-policy'),

    path('admin-view-policy-holder', views.admin_view_policy_holder_view,name='admin-view-policy-holder'),
    path('admin-view-approved-policy-holder', views.admin_view_approved_policy_holder_view,name='admin-view-approved-policy-holder'),
    path('admin-view-disapproved-policy-holder', views.admin_view_disapproved_policy_holder_view,name='admin-view-disapproved-policy-holder'),
    path('admin-view-waiting-policy-holder', views.admin_view_waiting_policy_holder_view,name='admin-view-waiting-policy-holder'),
    path('approve-request/<int:pk>', views.approve_request_view,name='approve-request'),
    path('reject-request/<int:pk>', views.disapprove_request_view,name='reject-request'),

    path('admin-question', views.admin_question_view,name='admin-question'),
    path('update-question/<int:pk>', views.update_question_view,name='update-question'),


#Customer

    path('customer_dashboard', views.customer_dashboard,name='customer_dashboard'),

    path('customer/apply_policy_view/', views.apply_policy_view, name='apply_policy_view'),
    path('apply/<int:pk>', views.apply_view,name='apply'),
    path('history', views.history_view,name='history'),

    path('ask-question', views.ask_question_view,name='ask-question'),
    path('question-history', views.question_history_view,name='question-history'),
    path('customer/payment2/<int:item_id>/', views.payment2, name='payment2'),
    path('select_customer/', views.select_customer, name='select_customer'),
    path('customer_details/<int:customer_id>/', views.customer_details, name='customer_details'),


    path('staff-view-policy-holder', views.staff_view_policy_holder_view,name='staff-view-policy-holder'),
    path('staff-view-approved-policy-holder', views.staff_view_approved_policy_holder_view,name='staff-view-approved-policy-holder'),
    path('staff-view-disapproved-policy-holder', views.staff_view_disapproved_policy_holder_view,name='staff-view-disapproved-policy-holder'),
    path('staff-view-waiting-policy-holder', views.staff_view_waiting_policy_holder_view,name='staff-view-waiting-policy-holder'),
    path('staff-request/<int:pk>', views.staff_approve_request_view,name='staff-approve-request'),
    path('staff-request/<int:pk>', views.staff_disapprove_request_view,name='staff-reject-request'),

    # path('staff-question', views.staff_question_view,name='staff-question'),
    # path('staff-update-question/<int:pk>', views.staff_update_question_view,name='staff-update-question'),

    #path('register-office/', views.office_registration, name='register_office'),
    path('register/', views.register_staff, name='register'),
    path('satffhome/',views.staff_home,name="staffhome"),
    path('add-agent/', views.add_agent, name='add-agent'),
    path('agenthome/', views.agenthome, name='agenthome'),
    path('register_office', views.register_office, name='register_office'),
    path('office_success/<int:office_id>/', views.office_detail, name='office_success'),  # New URL for showing office details
    path('view_office/', views.view_office, name='view_office'),
    path('register-staff/', views.register_staff, name='register_staff'),
    path('admin-staff-registration-successful/', views.admin_staff_registration_successful, name='admin_staff_registration_successful'),
    path('list-offices/', views.list_offices, name='list_offices'),
    path('vehicle-plan-registration/', views.vehicle_plan_registration, name='vehicle_plan_registration'),
    path('healthplanreg2/', views.health_plan_registration, name='health_plan_registration'),

#customer end
    path('register_policy/', views.register_vehicle_policy, name='register_policy'),
    path('policy_success/', views.policy_success, name='policy_success'),



]