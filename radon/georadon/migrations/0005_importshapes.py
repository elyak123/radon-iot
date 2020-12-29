# Generated by Django 2.2.10 on 2020-12-08 01:12

from django.db import migrations
from radon.georadon.utils import import_shapes


def importar_geografia(apps, schema_editor):
    import_shapes('ags_jm', 'ags_jm_loc')


class Migration(migrations.Migration):

    dependencies = [
        ('georadon', '0004_auto_20201207_1835'),
    ]

    operations = [
        migrations.RunPython(importar_geografia),
    ]
