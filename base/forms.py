from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm  
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget 
#from django.contrib.auth.models import User



class MyUserCreationForm(UserCreationForm):

    phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='BD'))
    class Meta:
        model = User 
        fields = ['name','username','email','phone_number','password1','password2']