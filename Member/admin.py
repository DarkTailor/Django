from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Member

class CustomMemberAdmin(UserAdmin):
    list_display = ('username', 'email', 'name', 'surname', 'telephone', 'location', 'new_believer_school', 'pays_tithe', 'working', 'schooling')
    fieldsets = (
        # ... (your custom fieldsets here)
    )
    add_fieldsets = (
        # ... (your custom add_fieldsets here)
    )

# Unregister the default UserAdmin for Member
admin.site.unregister(Member)

# Register the Member model with the custom admin class
admin.site.register(Member, CustomMemberAdmin)
