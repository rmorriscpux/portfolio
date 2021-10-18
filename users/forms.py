from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

user_valid = RegexValidator(regex=r"^[a-zA-Z]\w+$", message="Username must begin with a letter and only contain letters, numbers, or '_'")
name_valid = RegexValidator(regex=r"^[a-zA-Z][a-zA-Z\-']*$")
pw_error = "Password must contain one uppercase letter, one lowercase letter, one number, and one special character (e.g. #, $, %)"
pw_valid = [
    RegexValidator(regex=r".*[a-z].*", message=pw_error),
    RegexValidator(regex=r".*[A-Z].*", message=pw_error),
    RegexValidator(regex=r".*[0-9].*", message=pw_error),
    RegexValidator(regex=r".*\W.*", message=pw_error),
]

class Login(forms.Form):
    username = forms.CharField(max_length=45, min_length=3)
    password = forms.CharField(max_length=255, min_length=8, widget=forms.widgets.PasswordInput)

class Register(forms.Form):
    username = forms.CharField(max_length=45, min_length=3, validators=[user_valid])
    password = forms.CharField(max_length=255, min_length=8, widget=forms.widgets.PasswordInput, validators=pw_valid)
    confirm_pw = forms.CharField(max_length=255, min_length=8, label="Confirm Password", widget=forms.widgets.PasswordInput) # confirm_pw validation done in clean() below.
    email = forms.EmailField(max_length=255, label="Email Address")
    first_name = forms.CharField(max_length=45, validators=[name_valid])
    last_name = forms.CharField(max_length=45, validators=[name_valid])

    def clean(self):
        cleaned_data = super().clean()
        # Password Check
        if 'password' in cleaned_data and 'confirm_pw' in cleaned_data:
            if cleaned_data.get('password') != cleaned_data.get('confirm_pw'):
                self.add_error('confirm_pw', ValidationError("Passwords do not match."))