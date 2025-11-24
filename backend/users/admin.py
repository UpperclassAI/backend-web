from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, School

# Register the School model first
@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'created_at')
    search_fields = ('name', 'city')

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    # The fields to be used in displaying the User model.
    # These override the defaults of the standard Django User model.
    list_display = ('email', 'first_name', 'last_name', 'role', 'school', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role', 'school')
    ordering = ('email',)
    search_fields = ('email', 'first_name', 'last_name')

    # Fields to display on the add/change forms
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'role', 'school')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fields to display on the Add User form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'school', 'is_staff', 'is_superuser', 'password', 'password2'),
        }),
    )
    
    # Map USERNAME_FIELD to the email field
    # (The standard UserAdmin expects 'username')
    UserAdmin.fieldsets = fieldsets
    UserAdmin.add_fieldsets = add_fieldsets
    
admin.site.register(CustomUser, CustomUserAdmin)