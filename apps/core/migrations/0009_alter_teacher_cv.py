# Generated by Django 4.2.6 on 2024-07-22 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_generatedimage_delete_imagedalle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='cv',
            field=models.FileField(blank=True, default=None, null=True, upload_to='uploads/'),
        ),
    ]
