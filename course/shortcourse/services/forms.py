from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email','first_name', 'last_name', 'educational_background', 'password1','password2']

class profileUpdateForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    educational_background = forms.Textarea()
    image = forms.ImageField()
    cnic  = forms.CharField(label="CNIC")

    class Meta:
        model= User
        fields = ['email','first_name', 'last_name', 'cnic', 'contact','educational_background', 'image', ]