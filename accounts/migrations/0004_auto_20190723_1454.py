# Generated by Django 2.2.3 on 2019-07-23 14:54

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20190723_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other'), ('P', 'I prefer not to say')], max_length=1),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='linkedin',
            field=models.URLField(blank=True),
        ),
    ]
