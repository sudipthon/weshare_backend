from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# class CustomUserAdmin(UserAdmin):
#     model = User
#     list_display = ['email', 'username', 'is_active', 'is_verified','display_groups']
#     fieldsets = UserAdmin.fieldsets + (
#             (None, {'fields': ('is_verified',)}),
#     )

#     def display_groups(self, obj):
#         return ", ".join([group.name for group in obj.groups.all()])
#     display_groups.short_description = 'Groups'

# admin.site.register(User, CustomUserAdmin)
admin.site.register(User)