from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class BlogRegisterForm(UserCreationForm):
    name = forms.CharField(max_length=30,  required=False, help_text='Your name')
    email = forms.EmailField(help_text='Your email')

    class Meta:
        model = User
        fields = ('email', 'name', 'password1', 'password2')


class BlogTextForm(forms.ModelForm):
    title = forms.CharField(max_length=100, required=False, help_text='Заголовок')
    body = forms.CharField()

    class Meta:
        model = Post
        fields = ('title', 'body',)

