# Generated by Django 3.2.9 on 2021-11-30 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranker', '0014_alter_practice_swimmers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='practice',
            name='date',
            field=models.DateField(unique=True),
        ),
    ]