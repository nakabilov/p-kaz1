from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Smi, News, Comment


class CreateSmi(UserCreationForm):
    class Meta:
        model = Smi
        fields = ['email', 'company_name', 'insta', 'site_url', 'password1', 'password2', 'status']
        

class ChangeSmi(UserChangeForm):
    class Meta:
        model = Smi
        fields = ['email', 'company_name', 'insta', 'site_url', 'password', 'status']
        

class NewsForms(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'desc', 'petition', 'author', 'image', 'file', 'views', 'like']
        exclude = ['created_at']


class CommentForms(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        exclude = ['created_at']