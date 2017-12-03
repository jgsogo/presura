# Generated by Django 2.0rc1 on 2017-12-03 18:46

import datasets.utils.plottable
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('datasets', '0002_auto_20171203_1658'),
    ]

    operations = [
        migrations.CreateModel(
            name='Layer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('spatial_reference', models.IntegerField(choices=[(4326, 'WGS84'), (23030, 'Proyección UTM ED50 Huso 30 N')], default=4326)),
                ('draw_type', models.IntegerField(choices=[(0, 'Line'), (1, 'Filled')], default=0)),
                ('color_pattern', models.IntegerField(choices=[(0, 'Random')], default=0)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datasets.DataSet')),
            ],
            bases=(datasets.utils.plottable.Plottable, models.Model),
        ),
    ]
