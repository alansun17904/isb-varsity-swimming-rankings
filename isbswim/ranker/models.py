from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Extended profile that contains coach flag, which enables them to
    freely access and modify the database.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.CharField(max_length=5)
    attendance = models.BooleanField(default=False)
    is_coach = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Entry(models.Model):
    swimmer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    rank = models.IntegerField(default=0)
    event = models.CharField(max_length=10)
    time = models.FloatField()
    meet = models.CharField(max_length=50)

    def __str__(self):
        return f'{str(self.swimmer)} - {self.event}'

class Hyperparameters(models.Model):
    """Singleton Django Model"""

    h_index = models.IntegerField(default=6)
    attendance_bonus = models.BooleanField(default=False)
    attendance_weight = models.FloatField(default=0.02)
    weight_type = models.CharField(max_length=10, default="polynomial")
    weight_a = models.FloatField(default=2)
    bonus_matrix = models.JSONField()

    def __str__(self):
        return f'h={self.h_index}, wt={self.weight_type}, a={self.weight_a}'
