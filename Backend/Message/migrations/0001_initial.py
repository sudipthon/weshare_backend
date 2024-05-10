# Generated by Django 5.0.4 on 2024-05-01 02:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Account', '0002_alter_user_options_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participants', models.ManyToManyField(related_name='conversations', to='Account.user')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(default='default.jpg', upload_to='images/messages')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Account.user')),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='Message.conversation')),
            ],
        ),
    ]
