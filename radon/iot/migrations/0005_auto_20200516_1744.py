# Generated by Django 2.2.10 on 2020-05-16 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0004_dispositivo_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wisol',
            name='pac',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name='wisol',
            name='serie',
            field=models.CharField(max_length=8, unique=True),
        ),
    ]
