# Generated by Django 2.2.10 on 2020-04-13 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0005_auto_20200411_1801'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dispositivo',
            name='deviceTypeId',
        ),
        migrations.RemoveField(
            model_name='dispositivo',
            name='pac',
        ),
        migrations.RemoveField(
            model_name='dispositivo',
            name='prototype',
        ),
        migrations.RemoveField(
            model_name='dispositivo',
            name='serie',
        ),
        migrations.CreateModel(
            name='Wisol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serie', models.CharField(max_length=45, unique=True)),
                ('pac', models.CharField(max_length=80)),
                ('prototype', models.BooleanField(default=True)),
                ('deviceTypeId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iot.DeviceType')),
            ],
            options={
                'verbose_name': 'Wisol',
                'verbose_name_plural': 'Wisols',
            },
        ),
        migrations.AddField(
            model_name='dispositivo',
            name='wisol',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='iot.Wisol'),
            preserve_default=False,
        ),
    ]