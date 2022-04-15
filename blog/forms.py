from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Post, Comments, PostOption
 
class PostForm(ModelForm):
    ''' To create and update a post '''
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['date_posted','author','verification', 'group', 'type']

        widgets = {
            'image': forms.FileInput(),
            'content': forms.Textarea(attrs={'class':'form-control'}),
        }


class CommentForm(ModelForm):
    ''' To create and update a comment '''
    class Meta:
        model = Comments
        fields = ['content']

        widgets = {
            'content': forms.Textarea(attrs={
                'class':'comment-form-input', 'rows':'2', 'cols':'40'
                })
        }


      