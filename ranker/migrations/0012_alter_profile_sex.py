# Generated by Django 3.2.9 on 2021-11-27 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranker', '0011_entry_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='sex',
            field=models.CharField(max_length=6),
        ),
    ]
