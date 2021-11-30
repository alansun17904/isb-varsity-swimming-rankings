from django import forms
from ranker.forms import events, EntryFormAdmin
from ranker.forms import HyperparameterForm, ProfileFormAdmin
from django.contrib import admin
from ranker.models import Profile, Entry, Hyperparameters, Practice
from ranker.templatetags.extras import shorttolong


# Register your models here.


@admin.action(description="Approve user times")
def approve_entry(modeladmin, request, queryset):
    for entry in queryset:
        entry.approved = True
        modeladmin.save_model(request, entry, None, None)

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
    list_display = ['swimmer', 'sex', 'event', 'get_time', 'meet', 'approved']
    actions = [approve_entry]
    form = EntryFormAdmin

    def sex(self, obj):
        return obj.swimmer.sex

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
        for index, entry in enumerate(Entry.objects.filter(event=obj.event,
                swimmer__sex=obj.swimmer.sex, approved=True).order_by('time')):
            entry.rank = index + 1
            entry.save()

admin.site.register(Entry, EntryAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Hyperparameters, HyperparametersAdmin)
admin.site.register(Practice)
