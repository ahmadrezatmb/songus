# Generated by Django 3.2.6 on 2021-08-13 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_alter_group_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='joincode',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
