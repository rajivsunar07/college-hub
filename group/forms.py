from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Group
 

class CreateGroupForm(ModelForm):
    ''' Form to create a group '''
    class Meta:
        model = Group
        fields = ['group_type']

        widgets = {
            'group_type': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Group Type'})
        }
