# Generated by Django 3.2.5 on 2021-07-24 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mazebolt_project', '0002_test_command'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instance',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='test',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]