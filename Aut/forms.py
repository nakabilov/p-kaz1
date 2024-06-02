from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import People
from django import forms


class CreatePeopleForms(UserCreationForm):
    class Meta:
        model = People
        fields = ('last_name', 'first_name', 'father_name', 'iin', 'city', 'image', 'password', 'status', 'email')

class ChangePeopleForms(UserChangeForm):
    class Meta:
        model = People
        fields = ('last_name', 'first_name', 'father_name', 'iin', 'city', 'image', 'password', 'status', 'email')
        
     
class CityForms(forms.Form):
    class Meta:
        model = People
        fields = ('city')