from django import forms
from .models import * 
# creating a form
class Userform(forms.ModelForm):

    class Meta:
        model= User
        fields= ('first_name','last_name','email','cnic','contact','educational_background')