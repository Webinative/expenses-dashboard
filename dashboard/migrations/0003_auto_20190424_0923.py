# Generated by Django 2.2 on 2019-04-24 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20190423_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='amount',
            field=models.IntegerField(help_text='Value in subunits. 1 unit = 100 subunits.'),
        ),
    ]
