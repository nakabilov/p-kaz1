from django.contrib import admin
from .models import Petition, CategoryPetition, Image

admin.site.register(Petition)
admin.site.register(CategoryPetition)
