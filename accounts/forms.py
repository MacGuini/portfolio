from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class EmailVerificationForm(forms.Form):
	email = forms.EmailField()
	email.widget.attrs.update({'placeholder': 'Enter your email here', "class": "bg-transparent focus:border-blue-600 focus:ring border-0 border-b-2 border-slate-300 text-slate-500 mx-auto"})

class CustomUserCreationForm(UserCreationForm): # Inherets all aspects of the imported UserCreationForm
	first_name = forms.CharField()
	last_name = forms.CharField()
	email = forms.EmailField()
	# captcha = ReCaptchaField(widget=ReCaptchaV3())

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
		self.fields['first_name'].widget.attrs.update({'name': 'floating_first_name', 'id': 'floating_first_name', 'type': 'text'})
		self.fields['last_name'].widget.attrs.update({'name': 'floating_last_name', 'id': 'floating_last_name', 'type': 'text'})
		self.fields['email'].widget.attrs.update({'name': 'floating_email', 'id': 'floating_email', 'type': 'text'})
		self.fields['username'].widget.attrs.update({'name': 'floating_username', 'id': 'floating_username', 'type': 'text'})
		self.fields['password1'].widget.attrs.update({'name': 'floating_password', 'id': 'floating_password', 'type': 'password'})
		self.fields['password2'].widget.attrs.update({'name': 'repeat_password', 'id': 'floating_repeat_password', 'type': 'password'})
		for name, field in self.fields.items():
			field.widget.attrs.update({'class': 'input block py-2.5 px-0 w-full text-sm bg-transparent border-0 border-b-2 appearance-none text-white border-gray-600 focus:border-blue-500 focus:outline-none focus:ring-0 peer', 'placeholder': ' '})


class ProfileForm(forms.ModelForm):
	


	class Meta:
		model = Profile
		fields = '__all__'
		exclude = [
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