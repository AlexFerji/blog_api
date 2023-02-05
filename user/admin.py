from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Profile


class CustomUserAdmin(UserAdmin):
    add_form_template = "admin/auth/user/add_form.html"
    model = CustomUser
    list_display = ('username', 'email',  'is_staff', 'is_active')
    list_filter = ('username', 'email', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('user', 'first_name', 'last_name', 'birth_date', )
    list_filter = ('user', 'first_name', 'last_name', 'birth_date', )

admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)