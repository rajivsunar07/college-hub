from django.forms import ModelForm
from django import forms
from .models import Planner


class PlannerForm(ModelForm):
    ''' Form to create a plan '''
    class Meta:
        model = Planner
        fields = ('title', 'date', 'time')

        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Plan'} ),
            'date': forms.SelectDateWidget(attrs={'type':'date'}),
            'time': forms.TimeInput(attrs={'type':'time'})
        }
