# Generated by Django 2.2.10 on 2020-11-22 21:57

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clave', models.CharField(max_length=15)),
                ('nombre', models.CharField(max_length=30)),
                ('geo', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='georadon.Estado')),
            ],
        ),
    ]
