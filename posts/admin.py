from .models import Post, Comment
from django.contrib import admin


@admin.register(Post)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'date_posted', 'date_updated')
    search_fields = ('title', 'body')
    list_filter = ('user', 'date_posted', 'date_updated')
    ordering = ('-date_posted', '-date_updated')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'date_posted', 'date_updated')
    search_fields = ('body', )
    list_filter = ('author', 'date_posted', 'date_updated', 'post__title')
    ordering = ('-date_posted', '-date_updated')
