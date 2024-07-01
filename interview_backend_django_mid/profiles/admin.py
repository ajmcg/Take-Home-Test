from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile

class UserProfileAdmin(UserAdmin):
    """
    Custom admin interface for UserProfile model.
    """
    model = UserProfile
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'is_admin')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'first_name', 'last_name', 'avatar')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'is_admin', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active', 'is_admin')}
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)

admin.site.register(UserProfile, UserProfileAdmin)