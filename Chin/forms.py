from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Chin, PetitionAnswer
from django import forms


class CreateChinForm(UserCreationForm):
    class Meta:
        model = Chin
        fields = ['username', 'email', 'password2','password1',  'city', 'category', 'iin', 'status']
        

class ChangeChinForm(UserChangeForm):
    class Meta:
        model = Chin
        fields = ['username', 'email', 'password', 'city', 'category']
        


class PetitionAnswerForm(forms.ModelForm):
    class Meta:
        model = PetitionAnswer
        fields = ['chinov', 'petition', 'text', 'created_at']
        exclude = ['created_at']

