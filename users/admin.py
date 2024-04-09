from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile
from Member.models import Member

class CustomMemberAdmin(UserAdmin):
    list_display = ('username', 'email', 'name', 'surname', 'telephone', 'location', 'new_believer_school', 'pays_tithe', 'working', 'schooling')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('name', 'surname', 'email', 'telephone', 'location', 'new_believer_school', 'pays_tithe', 'working', 'schooling')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

# Register the Member model with the custom admin class
admin.site.register(Member, CustomMemberAdmin)

admin.site.register(UserProfile)
