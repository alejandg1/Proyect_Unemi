# Generated by Django 4.2.6 on 2024-07-20 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_user_username_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
