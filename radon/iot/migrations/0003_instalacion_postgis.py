# Generated by Django 2.2.10 on 2020-05-12 15:51
from django.db import migrations
from django.contrib.postgres.operations import CreateExtension

class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0002_auto_20200512_1050'),
    ]

    operations = [
        CreateExtension('postgis'),
    ]