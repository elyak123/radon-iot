# Generated by Django 2.2.10 on 2020-05-15 21:46

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import dynamic_validator.field_validation.validator


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('iot', '0004_dispositivo_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jornada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now=True)),
                ('gasera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Gasera')),
            ],
            options={
                'verbose_name': 'Jornada',
                'verbose_name_plural': 'Jornadas',
            },
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placa', models.CharField(max_length=12)),
                ('n_economico', models.CharField(blank=True, max_length=12)),
                ('operador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Vehiculo',
                'verbose_name_plural': 'Vehiculos',
            },
        ),
        migrations.CreateModel(
            name='Ruta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geometry', django.contrib.gis.db.models.fields.LineStringField(srid=4326)),
                ('jornada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rutas.Jornada')),
                ('vehiculo', models.ManyToManyField(to='rutas.Vehiculo')),
            ],
            options={
                'verbose_name': 'Ruta',
                'verbose_name_plural': 'Rutas',
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now=True)),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=12)),
                ('orden', models.IntegerField(null=True, verbose_name='Orden del dispositivo dentro de una ruta.')),
                ('dispositivo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iot.Dispositivo')),
                ('ruta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rutas.Ruta')),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
            },
            bases=(dynamic_validator.field_validation.validator.ModelFieldRequiredMixin, models.Model),
        ),
    ]