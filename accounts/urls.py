from django.urls import path 
from . import views 
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.index, name='index'),
	path('login/', views.loginUser, name='login'),
	path('logout/', views.logoutUser, name='logout'),
    path('register-account/', views.registerUser, name='register-account'),
    path('edit-account/', views.editAccount, name='edit-account'),
    path('verify-email/<str:pk>/<str:token>/', views.verifyEmail, name='verify-email'),
    path('verify-success/', TemplateView.as_view(template_name="accounts/verify_success.html"), name="verify-success"),
    path('validate-email/', views.newEmailVerification, name="validate-email"),
    path("confirm-email-notice/", TemplateView.as_view(template_name="accounts/confirm_email_notice.html"), name="confirm-email-notice"),
    path('blacklist/', views.blacklistIP, name='blacklist'),
    path('blacklisted/', views.blacklisted, name='blacklisted'),
] 