from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import ChangeSmi, CreateSmi
from .models import Smi, News, Comment

class CustomSmiAdmin(UserAdmin):
    add_form = CreateSmi
    form = ChangeSmi
    model = Smi
    list_display = ('email', 'company_name', 'insta', 'site_url' ,'is_superuser', 'is_staff', 'is_active', 'status')
    list_filter = ('is_superuser', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('status', 'email', 'company_name', 'insta', 'site_url', 'password', 'is_superuser')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
               'email', 'status', 'company_name', 'insta', 'site_url', 'password1', 'password2', 'is_superuser', 'is_staff', 'is_active')}
         ),
    )


admin.site.register(Smi, CustomSmiAdmin)
admin.site.register(Comment)
