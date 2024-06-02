from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Petition, CategoryPetition, Signature


class PetitionForm(forms.ModelForm):
    class Meta:
        model = Petition
        fields = ['title', 'description', 'author', 'img', 'file', 'category']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = CategoryPetition
        fields = ['petition', 'category']
        

class SignatureForm(forms.ModelForm):
    class Meta:
        model = Signature
        fields = ['petition', 'people', 'created_at']
    
    