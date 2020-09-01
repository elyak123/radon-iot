# Generated by Django 2.2.10 on 2020-08-31 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0007_instalacion_folio'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lectura',
            old_name='nivel',
            new_name='sensor',
        ),
        migrations.AddField(
            model_name='lectura',
            name='porcentaje',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
            preserve_default=False,
        ),
    ]