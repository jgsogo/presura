# Generated by Django 2.0rc1 on 2017-12-03 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='image_dpi',
        ),
        migrations.RemoveField(
            model_name='dataset',
            name='image_lw',
        ),
    ]
