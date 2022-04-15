from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile
 
class CreateUserForm(UserCreationForm):
    ''' Form to create a user'''
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'password1': forms.PasswordInput(attrs={'class':'form-control'}),
            'password2': forms.PasswordInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
        }


class UserUpdateForm(forms.ModelForm):
    '''Form to update a user'''
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}),
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}),
        }


class ProfileUpdateForm(forms.ModelForm):
    ''' Form to update profile '''
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']
  
        widgets = {
            'college_id': forms.TextInput(attrs={'class':'form-control', 'placeholder':'College ID'}),
            'user_type': forms.TextInput(attrs={'class':'form-control', 'placeholder':'User Type'}),
        }


class PictureUpdateForm(forms.ModelForm):
    ''' Form to update profile pictures '''
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user', 'college_id', 'user_type']
