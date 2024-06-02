from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import People, City
from .forms import CreatePeopleForms, ChangePeopleForms



class CustomPeopleAdmin(UserAdmin):
    add_form = CreatePeopleForms
    form = ChangePeopleForms
    model = People
    list_display = ('username', 'email', 'password', 'is_superuser', 'is_staff', 'is_active', 'iin', 'city', 'status')
    list_filter = ('is_superuser', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'is_superuser', 'status')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'status', 'iin','email','city', 'password1', 'password2', 'is_superuser', 'is_staff', 'is_active')}
         ),
    )


admin.site.register(People, CustomPeopleAdmin)
admin.site.register(City)
