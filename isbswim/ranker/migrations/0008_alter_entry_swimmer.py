# Generated by Django 3.2.9 on 2021-11-25 04:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ranker', '0007_auto_20211125_0353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='swimmer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ranker.profile'),
        ),
    ]