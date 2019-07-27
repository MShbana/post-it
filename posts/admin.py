from .models import Post
from django.contrib import admin


@admin.register(Post)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'slug', 'body')
    search_fields = ('title', 'body')
    list_filter = ('user', 'created', 'updated')

