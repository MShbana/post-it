from .utils import unique_slugify
from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    user = models.ForeignKey(
                User,
                on_delete=models.CASCADE,
                related_name='posts'
    )
    title = models.CharField(max_length=250, null=False, blank=False)
    likes = models.ManyToManyField(User, related_name='likes')
    slug = models.SlugField(unique=True, blank=True)
    body = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    @property
    def total_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ('-date_posted',)

    def __repr__(self):
        return f"<Post: user='{self.user}', title='{self.title}'>"

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        slug_str = f'{self.title}'
        unique_slugify(self, slug_str)
        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(
                Post,
                on_delete=models.CASCADE,
                related_name='comments'
    )
    author = models.ForeignKey(
                User,
                on_delete=models.CASCADE,
                related_name='total_comments'
    )
    body = models.CharField(max_length=250)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_posted', )

    def __repr__(self):
        return f"<Comment: post='{self.post}', body='{self.body}'>"

    def __str__(self):
        return f'Comment by: {self.author} on {self.post}'
