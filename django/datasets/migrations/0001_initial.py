# Generated by Django 2.0rc1 on 2017-12-07 10:49

import datasets.models._plottable
import datasets.models.author
import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('type', models.IntegerField(blank=True, choices=[(0, 'person'), (1, 'institution'), (2, 'corporate')], null=True, verbose_name='type')),
                ('url', models.URLField(blank=True, null=True, verbose_name='url')),
            ],
        ),
        migrations.CreateModel(
            name='Commandline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('user', models.CharField(max_length=64)),
                ('hostname', models.CharField(max_length=64)),
                ('info', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('license', models.CharField(blank=True, max_length=64, null=True, verbose_name='license')),
                ('is_public', models.NullBooleanField(verbose_name='is public')),
                ('description', models.TextField(blank=True, null=True)),
                ('published', models.DateField(blank=True, null=True, verbose_name='publish date')),
                ('url', models.URLField(blank=True, null=True, verbose_name='url')),
                ('object_id', models.PositiveIntegerField()),
                ('dataset_key', models.CharField(blank=True, help_text='Identification of this dataset inside the resource', max_length=64, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PadronCapitalProvincia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(blank=True, null=True), size=None)),
                ('ciudad', models.CharField(max_length=120)),
                ('men', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(blank=True, null=True), size=None)),
                ('women', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(blank=True, null=True), size=None)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PadronCCAA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(blank=True, null=True), size=None)),
                ('ccaa', models.CharField(max_length=120)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PadronIslas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(blank=True, null=True), size=None)),
                ('isla', models.CharField(max_length=120)),
                ('men', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(blank=True, null=True), size=None)),
                ('women', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(blank=True, null=True), size=None)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PadronMunicipios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(blank=True, null=True), size=None)),
                ('municipio', models.CharField(help_text='Usually postal code and name', max_length=120)),
                ('men', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(blank=True, null=True), size=None)),
                ('women', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(blank=True, null=True), size=None)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PadronProvincias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(blank=True, null=True), size=None)),
                ('provincia', models.CharField(max_length=120)),
                ('men', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(blank=True, null=True), size=None)),
                ('women', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(blank=True, null=True), size=None)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Shape',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=120)),
                ('polygons', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('rawData', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=120), size=None)),
            ],
        ),
        migrations.CreateModel(
            name='INEMap',
            fields=[
                ('dataset_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='datasets.Dataset')),
                ('fields', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), size=None)),
                ('key_field', models.CharField(max_length=64)),
                ('name_field', models.CharField(max_length=64)),
                ('key_field_name', models.CharField(max_length=64)),
                ('name_field_name', models.CharField(max_length=64)),
            ],
            bases=(datasets.models._plottable.PlottableCached, 'datasets.dataset'),
        ),
        migrations.CreateModel(
            name='INEPadron',
            fields=[
                ('dataset_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='datasets.Dataset')),
                ('map_type', models.CharField(max_length=128)),
                ('map', models.CharField(help_text='Matching map, must correspond to a Map::dataset_key', max_length=64)),
                ('units', models.CharField(max_length=64)),
                ('headings', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=64), size=None)),
                ('periods', django.contrib.postgres.fields.ArrayField(base_field=models.SmallIntegerField(), size=None)),
                ('categories', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=120), size=None)),
            ],
            bases=('datasets.dataset',),
        ),
        migrations.AddField(
            model_name='dataset',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=datasets.models.author.Author, to='datasets.Author'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='shape',
            name='map',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datasets.INEMap'),
        ),
        migrations.AddField(
            model_name='padronprovincias',
            name='padron',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datasets.INEPadron'),
        ),
        migrations.AddField(
            model_name='padronmunicipios',
            name='padron',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datasets.INEPadron'),
        ),
        migrations.AddField(
            model_name='padronislas',
            name='padron',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datasets.INEPadron'),
        ),
        migrations.AddField(
            model_name='padronccaa',
            name='padron',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datasets.INEPadron'),
        ),
        migrations.AddField(
            model_name='padroncapitalprovincia',
            name='padron',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datasets.INEPadron'),
        ),
    ]
