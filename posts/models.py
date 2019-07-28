from .utils import unique_slugify
from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=250, null=False, blank=False)
    slug = models.SlugField(unique=True, blank=True)
    body = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

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
