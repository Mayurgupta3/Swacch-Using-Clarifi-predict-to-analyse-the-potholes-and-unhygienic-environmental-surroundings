from django import forms
from models import User,PostModel


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields=['email','username','name','password']

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields=['image', 'caption']
