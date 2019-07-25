from .forms import UserRegisterationForm
from .models import UserProfile
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    
    list_display = ('user', 'slug', 'city', 'country', 'gender', 'linkedin')
    list_filter = ('created', 'gender', 'city', 'country')
    ordering = ('-created', 'user__username')
    search_fields = ('user__username', 'linkedin')
    prepopulated_fields = {'slug': ('user', )}


class CustomUserAdmin(UserAdmin):
    
    # form = UserUpdateForm
    add_form = UserRegisterationForm
    add_fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2'),}),)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
