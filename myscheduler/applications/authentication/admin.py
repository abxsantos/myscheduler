from django.contrib import admin

from myscheduler.applications.authentication.models import Client


@admin.register(Client)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ["id", "username", "cpf", "cpf_validation_status"]
