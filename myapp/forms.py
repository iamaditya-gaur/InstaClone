from django import forms
from models import SignUpModel, PostModel, LikeModel, CommentModel

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

class LikeForm(forms.ModelForm):

    class Meta:
        model = LikeModel
        fields = ['post_id']

class CommentForm(forms.ModelForm):

    class Meta:
        model = CommentModel
        fields = ['comment_text' , 'post_id']
