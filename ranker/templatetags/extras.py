from django import template

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
