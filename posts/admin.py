from .models import Post
from django.contrib import admin


@admin.register(Post)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'date_posted', 'date_updated')
    search_fields = ('title', 'body')
    list_filter = ('user', 'date_posted', 'date_updated')
    ordering = ('-date_posted', '-date_updated')

