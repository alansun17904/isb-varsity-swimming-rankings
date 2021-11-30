from django import forms
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """
    Extended profile that contains coach flag, which enables them to
    freely access and modify the database.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.CharField(max_length=6)
    attendance = models.BooleanField(default=False)
    is_coach = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return self.user.username == other.user.username

class Entry(models.Model):
    swimmer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    rank = models.IntegerField(default=0)
    event = models.CharField(max_length=10)
    time = models.FloatField()
    meet = models.CharField(max_length=50)
    approved = models.BooleanField(default=False)

    @classmethod
    def rerank(cls, sex, event, time):
        event = Entry.objects.filter(event=event,
                swimmer__sex=sex).order_by('time')
        rank = 0
        for entry in event:
            if event.time < time:
                rank += 1
        return rank + 1

    def __str__(self):
        return f'{str(self.swimmer)}: {self.event}'


class Hyperparameters(models.Model):
    """Singleton Django Model"""

    h_index = models.IntegerField(default=6)
    attendance_bonus = models.BooleanField(default=False)
    attendance_weight = models.FloatField(default=0.02)
    weight_type = models.CharField(max_length=10, default="polynomial")
    weight_a = models.FloatField(default=2)
    bonus_matrix = models.JSONField()

    def clean(self):
        if self.h_index < 1 or self.h_index > 12:
            raise forms.ValidationError("h-index must be >= 1 and <= 12.")
        elif self.attendance_weight < 0 or self.attendance_weight > 1:
            raise forms.ValidationError("attendance bonus must be between \
                        0 and 1.")

    def __str__(self):
        return f'h={self.h_index}, wt={self.weight_type}, a={self.weight_a}'

class Practice(models.Model):
    date = models.DateField(unique=True)
    swimmers = models.ManyToManyField(Profile, blank=True)

    def check_attendance(self, user):
        return user.username in [v.user.username for v in self.swimmers.all()]

    def __str__(self):
        return str(self.date)

