from django.db import models
from django.utils.translation import ugettext_lazy as _

from myscheduler.applications.authentication.models import Client


class Activity(models.Model):
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    key = models.CharField(max_length=255, null=False, blank=False)
    activity = models.CharField(max_length=255, null=False, blank=False)
    type = models.CharField(max_length=30, null=False, blank=False)
    participants = models.IntegerField(null=True)
    price = models.FloatField(null=False)
    link = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _("activity")
        verbose_name_plural = _("activities")
