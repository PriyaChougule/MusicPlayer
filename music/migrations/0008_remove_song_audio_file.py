# Generated by Django 3.1.4 on 2021-01-15 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0007_song_file_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='audio_file',
        ),
    ]
