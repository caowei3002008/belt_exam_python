from django import forms
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.core.validators import *
from models import *
import os, binascii, re
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')


class UserRegis(forms.ModelForm):
    name = forms.CharField()
    alias = forms.CharField()
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_pw = forms.CharField(widget=forms.PasswordInput)
    dob = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2018)))
    print dob

    class Meta:
        model = User
        fields = ('name', 'alias', 'email',  'dob', 'password')

    def clean_confirm_pw(self):
        cleaned_data = super(UserRegis, self).clean()
        pw = cleaned_data.get('password')
        cpw = cleaned_data.get('confirm_pw')
        print(cleaned_data)
        if pw != cpw:
            print(cleaned_data)
            raise forms.ValidationError("Your confirm password not mathing with the previous password.")
        elif len(pw) < 8:
            raise forms.ValidationError("Your password must at least 8 characters.")
        elif not PASSWORD_REGEX.match(pw):
            raise forms.ValidationError('Password must has at least one upper letter,one lower letter, and digit.')
        return self.cleaned_data

    def clean_name(self):
        cleaned_data = super(UserRegis, self).clean()
        user_name = cleaned_data.get('name')
        if len(user_name) < 4:
            raise forms.ValidationError("Your name must at least 4 characters.")
        elif any(char.isdigit() for char in user_name) is True:
            raise forms.ValidationError("Your name can not be number.")
        return self.cleaned_data.get('name')

    def clean_alias(self):
        cleaned_data = super(UserRegis, self).clean()
        user_alias = cleaned_data.get('alias')
        if len(user_alias) < 3:
            raise forms.ValidationError("Your alias must at least 3 characters.")
        elif any(char.isdigit() for char in user_alias) is True:
            raise forms.ValidationError("Your alias can not be number.")
        return self.cleaned_data.get('alias')


class login_form(forms.Form):
    email_login = forms.EmailField(widget=forms.EmailInput, label='Email')
    password_login = forms.CharField(widget=forms.PasswordInput, label='Password')
