# Generated by Django 3.2.9 on 2021-11-30 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ranker', '0015_alter_practice_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='rank',
        ),
    ]
