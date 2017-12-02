# Generated by Django 2.0rc1 on 2017-12-02 11:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DownloadLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('filename', models.FilePathField(editable=False, path='C:\\Javi\\dev\\presura\\data\\ine')),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.IntegerField(choices=[(0, 'Cartographic'), (1, 'Demographic')])),
                ('url', models.URLField()),
                ('available', models.BooleanField(default=True)),
                ('importer', models.CharField(blank=True, choices=[('mapas_municipales', 'mapas_municipales')], max_length=20, null=True, verbose_name='importer')),
            ],
        ),
        migrations.AddField(
            model_name='downloadlog',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ine.Resource'),
        ),
    ]
