from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import PersonManager


class Client(models.Model):
    """
    Custom Client model.

    The id consists of a telegram chat_id with the bot name.
    """

    class CPFValidationStatus(models.TextChoices):
        PENDING = ("pending", "Pending")
        INVALID = ("invalid", "Invalid")
        VALID = ("valid", "Valid")

    id = models.CharField(max_length=255, blank=False, null=False, unique=True, primary_key=True)
    username = models.CharField(_("username"), max_length=255, unique=False, blank=True, null=True)
    cpf = models.CharField(
        _("cpf"),
        max_length=11,
        blank=False,
        null=False,
    )
    cpf_validation_status = models.CharField(
        _("cpf validation status"),
        max_length=7,
        blank=False,
        null=False,
        choices=CPFValidationStatus.choices,
        default=CPFValidationStatus.PENDING,
    )
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    is_subscribed = models.BooleanField(_("has subscribed"), default=False)

    objects = PersonManager()

    class Meta:
        verbose_name = _("client")
        verbose_name_plural = _("clients")

    @property
    def has_valid_cpf(self):
        return True if self.cpf_validation_status == self.CPFValidationStatus.VALID else False

    @property
    def is_pending_validation(self):
        return True if self.cpf_validation_status == self.CPFValidationStatus.PENDING else False
