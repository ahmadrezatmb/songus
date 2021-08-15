# Generated by Django 3.2.6 on 2021-08-14 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0014_auto_20210814_1842'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personalplaylist',
            name='favoritve',
        ),
        migrations.AddField(
            model_name='personalplaylist',
            name='favoritve',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.songususer'),
        ),
    ]
