# Generated by Django 5.1.5 on 2025-01-19 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_HM', '0007_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='video/'),
        ),
    ]
