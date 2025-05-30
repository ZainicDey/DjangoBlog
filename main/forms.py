from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields=['title', 'description']
class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['content']
        labels = {
            'content': 'Your Comment',
        }