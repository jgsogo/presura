# Generated by Django 2.0rc1 on 2017-12-07 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0003_auto_20171207_1258'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dataset',
            options={'ordering': ['dataset_key']},
        ),
    ]
