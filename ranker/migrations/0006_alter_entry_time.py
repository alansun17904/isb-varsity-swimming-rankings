# Generated by Django 3.2.9 on 2021-11-25 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranker', '0005_entry_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='time',
            field=models.FloatField(),
        ),
    ]
