from django import forms
from models import SignUpModel

class SignUpForm(forms.ModelForm):

    class Meta:
        model = SignUpModel
        fields = ['email_mod','name_mod','username_mod','password_mod']

class LoginForm(forms.ModelForm):

    class Meta:
        model = SignUpModel
        fields = ['username_mod' , 'password_mod']
