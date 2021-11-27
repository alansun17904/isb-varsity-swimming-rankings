from django import forms
from ranker.forms import events, EntryFormAdmin
from ranker.forms import HyperparameterForm, ProfileFormAdmin
from django.contrib import admin
from ranker.models import Profile, Entry, Hyperparameters
from ranker.templatetags.extras import shorttolong

# Register your models here.


@admin.action(description="Approve user times")
def approve_entry(modeladmin, request, queryset):
    queryset.update(approved=True)

@admin.action(description="Approve user attendance")
def approve_attendance(modeladmin, request, queryset):
    queryset.update(attendance=True)

class HyperparametersAdmin(admin.ModelAdmin):
    form = HyperparameterForm

class ProfileAdmin(admin.ModelAdmin):
    list_filter = ['sex', 'attendance']
    list_display = ['user', 'sex', 'attendance', 'is_coach']
    actions = [approve_attendance]
    form = ProfileFormAdmin

class EntryAdmin(admin.ModelAdmin):
    list_filter = ['event', 'approved']
    list_display = ['swimmer', 'event', 'get_time', 'meet', 'approved']
    actions = [approve_entry]
    form = EntryFormAdmin

    def get_time(self, obj):
        return shorttolong(obj.time)

    def save_model(self, request, obj, form, change):
        # Delete previous entries.
        previous_entry = Entry.objects.filter(
                swimmer__user__username=obj.swimmer.user.username,
                event=obj.event
        )
        if len(previous_entry) != 0 and obj.time <= previous_entry[0].time:
            previous_entry[0].delete()
        obj.save()
        Entry.recalculate_entry_ranks(obj.swimmer.sex, obj.event)

admin.site.register(Entry, EntryAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Hyperparameters, HyperparametersAdmin)
