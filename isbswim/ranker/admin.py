from django.contrib import admin
from ranker.models import Profile, Entry, Hyperparameters
from ranker.templatetags.extras import shorttolong

# Register your models here.
admin.site.register(Profile)
admin.site.register(Hyperparameters)

@admin.action(description="Approve user times")
def approve_entry(modeladmin, request, queryset):
    queryset.update(approved=True)

class EntryAdmin(admin.ModelAdmin):
    list_filter = ['event', 'approved']
    list_display = ['swimmer', 'event', 'get_time', 'meet', 'approved']
    actions = [approve_entry]

    def get_time(self, obj):
        return shorttolong(obj.time)

    def save_model(self, request, obj, form, change):
        # Delete previous entries.
        previous_entry = Entry.objects.filter(
                swimmer__user__username=obj.swimmer.user.username,
                event=obj.event
        )
        previous_entry[0].delete()
        super().save_model(request, obj, form, change)
        Entry.recalculate_entry_ranks(obj.swimmer.sex, obj.event)


admin.site.register(Entry, EntryAdmin)
