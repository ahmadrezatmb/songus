# Generated by Django 3.2.6 on 2021-08-12 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_alter_group_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='member',
            field=models.ManyToManyField(blank=True, null=True, related_name='groupss', to='web.songususer'),
        ),
    ]
