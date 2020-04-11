# Generated by Django 2.2.10 on 2020-04-10 18:24

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0007_auto_20200404_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dispositivo',
            name='capacidad',
            field=models.IntegerField(null=True, verbose_name='Capacidad del tanque'),
        ),
        migrations.AlterField(
            model_name='dispositivo',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(null=True, srid=4326),
        ),
    ]
