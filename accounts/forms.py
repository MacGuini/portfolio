from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class CustomUserCreationForm(UserCreationForm): # Inherets all aspects of the imported UserCreationForm
	
	class Meta: 
		model = User
		fields = ['first_name', 'last_name', 'username','email', 'password1', 'password2']
		labels = {
		'first_name': 'First Name',
		'last_name': 'Last Name',
		'email': 'E-Mail',
		'username': 'Username',
		'password1': 'Password',
		'password2': 'Verify Password',
		}

	def __init__(self, *args, **kwargs):
		super(CustomUserCreationForm, self).__init__(*args, **kwargs)
		for name, field in self.fields.items():
			field.widget.attrs.update({'class': 'input'})


class ProfileForm(forms.ModelForm):
	


	class Meta:
		model = Profile
		fields = '__all__'
		exclude = [
			'user',
			'is_superuser',
		]

		labels = {
			'fname':'First Name',
			'mname':'Middle Name',
			'lname':'Last Name',
			'street1':'Address',
			'street2':'Apt/Suite',
		}
		widgets = {
			'username':forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Username"}),
			'fname': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': "First Name"}),
			'mname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Middle Name"}),
			'lname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Last Name"}),
			'street1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Street Address"}),
			'street2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Apt/Suite"}),
			'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "City"}),
			'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "State"}),
			'zipcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Zipcode"}),
			'home': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Home Phone"}),
			'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Mobile Phone"}),
			'work': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Work Phone"}),
			'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "E-Mail"}),
			'preference': forms.RadioSelect(),
			'is_staff': forms.CheckboxInput(attrs={'class': 'check-box-lg'}),
			# 'is_superuser': forms.CheckboxInput(attrs={'class': 'check-box-lg'}),
		}
			
		# NOTE: This doesn't work for some reason
		# def __init__(self, *args, **kwargs):
		# 	super(ProfileForm, self).__init__(*args, **kwargs)

		# 	for name, field in self.fields.items():
		# 		field.widget.attrs.update({'class': 'input'})
		# 		field.widget.attrs.update({'class': 'form-control'})
		# 		field.widget.attrs.update({'class': 'p-2'})

	def clean_mobile(self, *args, **kwargs):
		mobile = self.cleaned_data.get("mobile")

		if mobile:
			if mobile.isdigit()==False:
				raise forms.ValidationError("Only Numbers")
		return mobile

	def clean_home(self, *args, **kwargs):
		home = self.cleaned_data.get("home")
		if home:
			if home.isdigit()==False:
				raise forms.ValidationError("Only Numbers")
		return home

	def clean_work(self, *args, **kwargs):
		work = self.cleaned_data.get("work")
		if work:
			if work.isdigit()==False:
				raise forms.ValidationError("Only Numbers")
		return work


	
