# Generated by Django 3.2.9 on 2021-11-25 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='time',
            field=models.CharField(max_length=10),
        ),
    ]