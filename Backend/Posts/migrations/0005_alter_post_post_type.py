# Generated by Django 5.0.4 on 2024-05-05 07:27

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0004_post_post_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_type',
            field=models.CharField(choices=[('Giveaway', 'Giveaway'), ('Exchange', 'Exchange')], default=django.utils.timezone.now, max_length=30),
            preserve_default=False,
        ),
    ]
