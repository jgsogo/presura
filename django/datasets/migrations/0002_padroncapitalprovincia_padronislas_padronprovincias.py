# Generated by Django 2.0rc1 on 2017-12-06 19:29

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PadronCapitalProvincia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(blank=True, null=True), size=None)),
                ('ciudad', models.CharField(max_length=120)),
                ('men', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(blank=True, null=True), size=None)),
                ('women', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(blank=True, null=True), size=None)),
                ('padron', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datasets.Padron')),
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
                ('padron', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datasets.Padron')),
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
                ('padron', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datasets.Padron')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
