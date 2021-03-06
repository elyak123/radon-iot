# Generated by Django 2.2.10 on 2020-12-07 01:47

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('georadon', '0003_auto_20201206_1947'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gasera',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=80, unique=True)),
            ],
            options={
                'verbose_name': 'Gasera',
                'verbose_name_plural': 'Gaseras',
            },
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=80)),
                ('numeroPermiso', models.CharField(max_length=22, unique=True)),
                ('ubicacion', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
                ('telefono', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('gasera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.Gasera')),
                ('localidad', models.ManyToManyField(to='georadon.Localidad')),
                ('municipio', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='georadon.Municipio')),
            ],
        ),
        migrations.CreateModel(
            name='Precio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=12)),
                ('fecha', models.DateTimeField(auto_now=True)),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.Sucursal')),
            ],
            options={
                'verbose_name': 'Precio',
                'verbose_name_plural': 'Precios',
            },
        ),
    ]
