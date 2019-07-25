from .models import UserProfile
from django.contrib import admin


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug', 'city', 'country', 'gender', 'linkedin')
    list_filter = ('created', 'gender', 'city', 'country')
    ordering = ('-created', 'user__username')
    search_fields = ('user__username', 'linkedin')
    prepopulated_fields = {'slug': ('user', )}
