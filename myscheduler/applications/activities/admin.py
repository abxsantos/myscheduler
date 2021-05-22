from django.contrib import admin

from myscheduler.applications.activities.models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    search_fields = []
