from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
	path('login/', views.loginUser, name='login'),
	path('logout/', views.logoutUser, name='logout'),
    path('accounts/register-account/', views.registerUser, name='register-account'),
] 