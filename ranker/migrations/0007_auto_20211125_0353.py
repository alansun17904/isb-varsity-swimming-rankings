# Generated by Django 3.2.9 on 2021-11-25 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranker', '0006_alter_entry_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='sex',
        ),
        migrations.AddField(
            model_name='profile',
            name='sex',
            field=models.CharField(default='MALE', max_length=5),
            preserve_default=False,
        ),
    ]
