from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, IP_Address, Blacklist

class EmailVerificationForm(forms.Form):
	email = forms.EmailField()
	email.widget.attrs.update({'name': 'floating_email', 'id': 'floating_email', 'type': 'text', 'class': 'input block py-2.5 px-0 w-full text-sm bg-transparent border-0 border-b-2 appearance-none text-white border-gray-600 focus:border-blue-500 focus:outline-none focus:ring-0 peer', 'placeholder': ' '})

class BlacklistForm(forms.Form):
	ip_address = forms.ModelMultipleChoiceField(
		queryset=IP_Address.objects.all(),
		widget=forms.CheckboxSelectMultiple,
		required=False,
		label="Select IP Addresses to Blacklist"
	)

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
        exclude = ['is_superuser']
        labels = {
            'fname':'First Name',
            'mname':'Middle Name',
            'lname':'Last Name',
            'street1':'Address',
            'street2':'Apt/Suite',
        }
        widgets = {
            'username': forms.TextInput(),
            'fname': forms.TextInput(),
            'mname': forms.TextInput(),
            'lname': forms.TextInput(),
            'street1': forms.TextInput(),
            'street2': forms.TextInput(),
            'city': forms.TextInput(),
            'state': forms.TextInput(),
            'zipcode': forms.TextInput(),
            'home': forms.TextInput(),   # or forms.TelInput() Haven't tested this yet but leaving the comment here for future reference
            'mobile': forms.TextInput(), # or forms.TelInput()
            'work': forms.TextInput(),   # or forms.TelInput()
            'email': forms.EmailInput(),
            'preference': forms.RadioSelect(),
            'is_staff': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        text_base = {
            'class': 'block w-full text-sm bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-900 dark:text-white focus:ring-blue-500 focus:border-blue-500 p-2.5',
        }
        checkbox_base = {'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500'}

        # apply Tailwind to all text-like fields
        for name in ['username','fname','mname','lname','street1','street2','city','state','zipcode','home','mobile','work','email']:
            if name in self.fields:
                self.fields[name].widget.attrs.update({**text_base})

        # nice placeholders
        placeholders = {
            'username': 'Username',
            'fname': 'First Name', 'mname': 'Middle Name', 'lname': 'Last Name',
            'street1': 'Street Address', 'street2': 'Apt/Suite',
            'city': 'City', 'state': 'State', 'zipcode': 'Zipcode',
            'home': 'Home Phone (digits only)',
            'mobile': 'Mobile Phone (digits only)',
            'work': 'Work Phone (digits only)',
            'email': 'you@example.com'
        }
        for k, v in placeholders.items():
            if k in self.fields:
                self.fields[k].widget.attrs.setdefault('placeholder', v)

        # radio group (preference)
        if 'preference' in self.fields:
            self.fields['preference'].widget.attrs.update({'class': 'space-y-2'})

        # is_staff checkbox
        if 'is_staff' in self.fields:
            self.fields['is_staff'].widget.attrs.update(checkbox_base)

    # phone validators
    def clean_mobile(self):
        mobile = self.cleaned_data.get("mobile")
        if mobile and not mobile.isdigit():
            raise forms.ValidationError("Only numbers")
        return mobile

    def clean_home(self):
        home = self.cleaned_data.get("home")
        if home and not home.isdigit():
            raise forms.ValidationError("Only numbers")
        return home

    def clean_work(self):
        work = self.cleaned_data.get("work")
        if work and not work.isdigit():
            raise forms.ValidationError("Only numbers")
        return work