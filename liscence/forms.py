from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Client

class UserRegisterForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class ClientCreateForm(forms.ModelForm):
	class Meta:
		model = Client
		field=''
		exclude = ('submitted', 'payload','captcha_text', 'session_text',)

