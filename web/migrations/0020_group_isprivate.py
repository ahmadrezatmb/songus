# Generated by Django 3.2.6 on 2021-08-14 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0019_song_recentmusic'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='isprivate',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]