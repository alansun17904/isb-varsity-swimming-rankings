# Generated by Django 3.2.9 on 2021-11-25 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranker', '0009_hyperparameters'),
    ]

    operations = [
        migrations.AddField(
            model_name='hyperparameters',
            name='attendance_weight',
            field=models.FloatField(default=0.02),
        ),
    ]
