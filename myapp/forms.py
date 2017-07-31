from django import forms
from models import SignUpModel, PostModel

class SignUpForm(forms.ModelForm):

    class Meta:
        model = SignUpModel
        fields = ['email_mod','name_mod','username_mod','password_mod']

class LoginForm(forms.ModelForm):

    class Meta:
        model = SignUpModel
        fields = ['username_mod' , 'password_mod']

class PostForm(forms.ModelForm):

    class Meta:
        model = PostModel
        fields = ['image', 'caption']
