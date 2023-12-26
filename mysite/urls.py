"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from .forms import CustomPasswordResetForm, CustomSetPasswordForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('forum/', include('forum.urls')),
    path("construction/", TemplateView.as_view(template_name="construction.html"), name="construction"),
    # Built in password reset views
    # User submits email for reset
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="reset_password.html", form_class=CustomPasswordResetForm), name="reset_password"),
    # Email sent message
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="reset_password_sent.html"), name="password_reset_done"),
    # Email with link and reset instructions
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reset.html", form_class=CustomSetPasswordForm), name="password_reset_confirm"),
    # Password successfully reset message
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_complete.html"), name="password_reset_complete"),
    
]

# NOTE: this line connects static urls to their respective settings
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)