# Generated by Django 3.2.6 on 2021-08-14 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0018_auto_20210814_2040'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='recentmusic',
            field=models.ManyToManyField(blank=True, null=True, related_name='recentmusic', to='web.songususer'),
        ),
    ]
