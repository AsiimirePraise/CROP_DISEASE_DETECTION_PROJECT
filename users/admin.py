# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ['phone', 'address', 'farmer','agronomist', 'extension_worker']

class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]

# Unregister the default User admin
admin.site.unregister(User)
# Register the new User admin with Profile inline
admin.site.register(User, CustomUserAdmin)

# Also register Profile separately if you want direct access
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'farmer','agronomist','extension_worker','address_preview']
    list_filter = ['farmer', 'agronomist', 'extension_worker']
    search_fields = ['user__username', 'user__email', 'phone']
    list_editable = ['farmer', 'agronomist', 'extension_worker']
    
    def address_preview(self, obj):
        if obj.address:
            return obj.address[:50] + '...' if len(obj.address) > 50 else obj.address
        return 'No address'
    address_preview.short_description = 'Address'


