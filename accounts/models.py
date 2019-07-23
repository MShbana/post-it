from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries import fields

class UserProfile(models.Model):


    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'I prefer not to say')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', blank=True)
    city = models.CharField(max_length=20)
    country = fields.CountryField()
    linkedin = models.URLField()
    gender =  models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return f'{self.user} Profile'

    def __repr__(self):
        return f"<UserProfile: user='{self.user}', image='{self.image}', city='{self.city}', country='{self.country}', linkedin='{self.linkedin}', gender='{self.gender}'>"

    class Meta:
        verbose_name_plural = 'Users Profiles'

    @receiver(post_save, sender=User)
    def create_userprofile(sender, instance, created, **kwargs):
        if created:
            user_profile = UserProfile(user=instance)
            user_profile.save()