# Generated by Django 2.2.4 on 2019-09-14 20:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20190914_2029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='image_description',
        ),
    ]
