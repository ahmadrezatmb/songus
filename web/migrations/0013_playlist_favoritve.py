# Generated by Django 3.2.3 on 2021-08-13 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0012_song_playlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='favoritve',
            field=models.ManyToManyField(blank=True, null=True, related_name='favorites', to='web.songususer'),
        ),
    ]