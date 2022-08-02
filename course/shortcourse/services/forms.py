from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email','first_name', 'last_name', 'educational_background', 'password1','password2']

class update_profile_form(forms.ModelForm):
    
    class Meta:
        model= User
        fields = ['email','first_name', 'last_name', 'educational_background']