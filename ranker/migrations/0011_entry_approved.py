# Generated by Django 3.2.9 on 2021-11-26 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranker', '0010_hyperparameters_attendance_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
