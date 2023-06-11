# customers/forms.py
from django import forms

class CustomerLoginForm(forms.Form):
    # create a login form with username and password fields
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
