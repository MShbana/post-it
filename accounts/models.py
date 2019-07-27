from django_countries import fields
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify


class Profile(models.Model):

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'I prefer not to say')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', blank=True)
    city = models.CharField(max_length=20, blank=True)
    country = fields.CountryField(blank=True)
    linkedin = models.URLField(blank=True)
    gender =  models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)

    class Meta:
        ordering = ('-created', )

    def __repr__(self):
        return f"<Profile: user='{self.user}', image='{self.image}', city='{self.city}', country='{self.country}', linkedin='{self.linkedin}', gender='{self.gender}'>"

    def __str__(self):
        return f'{self.user} Profile'

    def display_gender(self):
        if self.gender:
            return dict(self.GENDER_CHOICES)[self.gender]
        else:
            return None

    def get_model_fields(self):
        return [((field.name), field.value_to_string(self)) for field in self._meta.fields]


    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            user_profile = Profile(user=instance)
            user_profile.save()


    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.user)

        super().save(*args, **kwargs)
