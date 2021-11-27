# Generated by Django 3.2.9 on 2021-11-25 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranker', '0002_alter_entry_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='meet',
            field=models.CharField(default='none', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='attendance',
            field=models.BooleanField(default=False),
        ),
    ]
