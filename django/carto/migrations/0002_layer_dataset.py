# Generated by Django 2.0rc1 on 2017-12-06 19:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('carto', '0001_initial'),
        ('datasets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='dataset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datasets.Map'),
        ),
    ]
