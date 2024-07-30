from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from user.models import User, Permission


class PermissionAdmin(admin.ModelAdmin):
    list_display = ('level', 'description')
    search_fields = ('description',)
    list_filter = ('level',)


admin.site.register(Permission, PermissionAdmin)


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'username', 'permission')
    search_fields = ('email', 'username')
    list_filter = ('permission',)
    ordering = ('email',)
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'permission')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'permission'),
        }),
    )


admin.site.register(User, UserAdmin)
