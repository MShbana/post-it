from django_countries import fields
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from PIL import Image
from posts.utils import unique_slugify


class Profile(models.Model):

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'I prefer not to say')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(
                    'self',
                    related_name='followers',
                    symmetrical=False,
                    blank=True
    )
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(
                default='default.jpg',
                upload_to='profile_pics',
                blank=True
    )
    city = models.CharField(max_length=20, blank=True)
    country = fields.CountryField(blank=True)
    linkedin = models.URLField(blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)

    class Meta:
        ordering = ('-created', )

    def __repr__(self):
        return (
                "<Profile: "
                f"user='{self.user}', "
                f"image='{self.image}', "
                f"city='{self.city}', "
                f"country='{self.country}', "
                f"linkedin='{self.linkedin}', "
                f"gender='{self.gender}'>"
        )

    def __str__(self):
        return f'{self.user} Profile'

    def display_gender(self):
        if self.gender:
            return dict(self.GENDER_CHOICES)[self.gender]
        else:
            return None

    def save(self, *args, **kwargs):
        slug_str = f'{self.user}'
        unique_slugify(self, slug_str)
        super().save(*args, **kwargs)

        # This is commented for now because it will cause issues
        # when storing our files in AWS S3

        # if self.image:
        #     img = Image.open(self.image.path)
        #     if img.height > 300 or img.width > 300:
        #         output_size = (300, 300)
        #         img.thumbnail(output_size)
        #         img.save(self.image.path)

    def image_url(self):
        if (self.image and
                hasattr(self.image, 'url')):
            return self.image.url
