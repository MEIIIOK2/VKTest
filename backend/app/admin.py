from django.contrib import admin
from .models import CustomUser , Image
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
class CustomUserAdmin(BaseUserAdmin):
    ordering = ('email',)
    list_display = ( 'email',)
    model = CustomUser
    fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('email', 'first_name', 'last_name', 'password', 'is_staff','is_superuser'),
    }),
    )
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Image)