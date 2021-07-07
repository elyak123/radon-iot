# Generated by Django 2.2.10 on 2021-05-12 17:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0021_auto_20210512_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wisol',
            name='firmware',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iot.Hardware'),
        ),
        migrations.AlterField(
            model_name='wisol',
            name='hardware',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iot.Firmware'),
        ),
    ]