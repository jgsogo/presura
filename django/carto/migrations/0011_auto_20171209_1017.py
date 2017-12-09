# Generated by Django 2.0rc1 on 2017-12-09 09:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carto', '0010_auto_20171208_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='lw',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='map',
            name='alpha',
            field=models.FloatField(default=1.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)]),
        ),
        migrations.AddField(
            model_name='map',
            name='draw_type',
            field=models.IntegerField(choices=[(0, 'Line'), (1, 'Filled')], default=0),
        ),
        migrations.AddField(
            model_name='map',
            name='lw',
            field=models.FloatField(default=0.1),
        ),
        migrations.AlterField(
            model_name='map',
            name='_tile_map_base',
            field=models.CharField(blank=True, choices=[('CARTO_DARK_LABELS', 'CARTO_DARK_LABELS'), ('STAMEN_TONER_Background', 'STAMEN_TONER_Background'), ('STAMEN_TONER_Hybrid', 'STAMEN_TONER_Hybrid'), ('STAMEN_TERRAIN_Labels', 'STAMEN_TERRAIN_Labels'), ('OSM', 'OSM'), ('STAMEN_TONER_Labels', 'STAMEN_TONER_Labels'), ('STAMEN_TERRAIN_Lines', 'STAMEN_TERRAIN_Lines'), ('STAMEN_TONER_Lines', 'STAMEN_TONER_Lines'), ('CARTO_LIGHT', 'CARTO_LIGHT'), ('STAMEN_TONER_Lite', 'STAMEN_TONER_Lite'), ('CARTO_LIGHT_NOLABELS', 'CARTO_LIGHT_NOLABELS'), ('STAMEN_TONER', 'STAMEN_TONER'), ('CARTO_DARK_NOLABELS', 'CARTO_DARK_NOLABELS'), ('STAMEN_TERRAIN_Background', 'STAMEN_TERRAIN_Background'), ('CARTO_LIGHT_LABELS', 'CARTO_LIGHT_LABELS'), ('CARTO_DARK', 'CARTO_DARK'), ('STAMEN_TERRAIN', 'STAMEN_TERRAIN'), ('STAMEN_WATERCOLOUR', 'STAMEN_WATERCOLOUR')], max_length=64, null=True),
        ),
    ]
