# Generated by Django 2.2.10 on 2020-07-29 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20190809_0116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='media/default.jpg', upload_to='profile_pics'),
        ),
    ]
