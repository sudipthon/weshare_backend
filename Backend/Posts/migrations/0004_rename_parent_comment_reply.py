# Generated by Django 5.0.4 on 2024-05-25 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0003_comment_parent_alter_post_tags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='parent',
            new_name='reply',
        ),
    ]
