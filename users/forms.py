from django import forms
from django.core.validators import RegexValidator

user_valid = RegexValidator(regex=r"^[a-zA-Z]\w+$", message="Must begin with a letter and only contain letters, numbers, or '_'")
name_valid = RegexValidator(regex=r"^[a-zA-Z][a-zA-Z\-']*$")
pw_valid = [
    RegexValidator(regex=r".*[a-z].*"),
    RegexValidator(regex=r".*[A-Z].*"),
    RegexValidator(regex=r".*[0-9].*"),
    RegexValidator(regex=r".*\W.*"),
]

class Login(forms.Form):
    username = forms.CharField(max_length=45, min_length=3)
    password = forms.CharField(max_length=255, min_length=6, widget=forms.widgets.PasswordInput)

class Register(forms.Form):
    username = forms.CharField(max_length=45, min_length=3, validators=[user_valid])
    password = forms.CharField(max_length=255, min_length=8, widget=forms.widgets.PasswordInput, validators=pw_valid)
    confirm_pw = forms.CharField(max_length=255, min_length=8, label="Confirm Password", widget=forms.widgets.PasswordInput, validators=pw_valid)
    email = forms.EmailField(max_length=255, label="Email Address")
    first_name = forms.CharField(max_length=45, validators=[name_valid])
    last_name = forms.CharField(max_length=45, validators=[name_valid])
    birthdate = forms.DateField()