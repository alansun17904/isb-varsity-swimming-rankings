from django.contrib import admin
from ranker.models import Profile, Entry, Hyperparameters

# Register your models here.
admin.site.register(Profile)
admin.site.register(Entry)
admin.site.register(Hyperparameters)
