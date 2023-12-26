from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={
                'id':'email-field',
                'class': 'text-sm rounded-lg block w-full p-2.5 bg-gray-700 border-gray-600 placeholder-gray-400 text-white focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Enter Email',
            }
        )
    )

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        # Add your customizations here
        self.fields['new_password1'].label = ""
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={
            "class": "text-sm rounded-lg block w-full p-2.5 bg-gray-700 border-gray-600 placeholder-gray-400 text-white focus:ring-blue-500 focus:border-blue-500",
            "placeholder": "Enter New Password"
        })
        self.fields['new_password2'].label = ""
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={
            "class": "text-sm rounded-lg block w-full p-2.5 bg-gray-700 border-gray-600 placeholder-gray-400 text-white focus:ring-blue-500 focus:border-blue-500",
            "placeholder": "Confirm Password"            
            })