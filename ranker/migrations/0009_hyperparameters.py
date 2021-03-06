# Generated by Django 3.2.9 on 2021-11-25 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranker', '0008_alter_entry_swimmer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hyperparameters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('h_index', models.IntegerField(default=6)),
                ('attendance_bonus', models.BooleanField(default=False)),
                ('weight_type', models.CharField(default='polynomial', max_length=10)),
                ('weight_a', models.FloatField(default=2)),
                ('bonus_matrix', models.JSONField()),
            ],
        ),
    ]
