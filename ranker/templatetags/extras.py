from django import template
from ranker.models import Profile

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    return round(float(value) * arg)

@register.filter(name='shorttolong')
def shorttolong(value):
    if value < 60:
        return f'{round(value, 2):.2f}'
    else:
        minutes = value // 60
        seconds = int(value - minutes * 60)
        milliseconds = int((value - minutes * 60 - seconds) * 100)
        return f'{int(minutes)}:{round(seconds):02d}.{milliseconds:02d}'

@register.filter(name='check_attendance')
def check_attendance(value, user):
    return value.check_attendance(user)

@register.filter(name='is_coach')
def is_coach(user):
    p = Profile.objects.get(user__username=user.username)
    return p.is_coach


