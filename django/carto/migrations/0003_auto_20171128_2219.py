# Generated by Django 2.0rc1 on 2017-11-28 22:19

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carto', '0002_auto_20171126_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ccaa',
            name='points',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326),
        ),
        migrations.AlterField(
            model_name='country',
            name='points',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326),
        ),
        migrations.AlterField(
            model_name='municipality',
            name='points',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326),
        ),
        migrations.AlterField(
            model_name='province',
            name='points',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326),
        ),
    ]