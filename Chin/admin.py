from django.contrib.auth.admin import UserAdmin
from .models import Chin
from .forms import ChangeChinForm, CreateChinForm
from django.contrib import admin

# admin.site.register(ChinForm)




class CustomChinAdmin(UserAdmin):
    add_form = CreateChinForm
    form = ChangeChinForm
    model = Chin
    list_display = ('username', 'email', 'city', 'category', 'is_superuser', 'is_staff', 'is_active', 'status')
    list_filter = ('is_superuser', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'is_superuser', 'status')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'status', 'iin','email','city', 'category', 'password1', 'password2', 'is_superuser', 'is_staff', 'is_active')}
         ),
    )


admin.site.register(Chin, CustomChinAdmin)
