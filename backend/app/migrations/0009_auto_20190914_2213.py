# Generated by Django 2.2.4 on 2019-09-14 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_remove_message_image_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='message',
            name='resolved',
            field=models.BooleanField(default=False),
        ),
    ]
