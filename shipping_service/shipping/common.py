import uuid
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField

MAX_DECIMAL_DIGITS = 6


class BaseModelMixin(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = CreationDateTimeField(_("Created at"))
    updated_at = ModificationDateTimeField(_("Updated at"))

    class Meta:
        get_latest_by = "updated_at"
        ordering = (
            "-updated_at",
            "-created_at",
        )
        abstract = True

    @classmethod
    def model_fields(cls) -> list:
        return [field.name for field in cls._meta._get_fields(reverse=False)]


class PositiveDecimalField(models.DecimalField):
    description = _("Positive decimal field")
    help_text = _("Decimal field allowing only positive numbers")

    def __init__(self, *args, **kwargs):
        kwargs["max_digits"] = kwargs.get("max_digits", MAX_DECIMAL_DIGITS)
        kwargs["decimal_places"] = kwargs.get("decimal_places", 2)
        kwargs["validators"] = kwargs.get('validators', [MinValueValidator(Decimal("0.00"))])
        super().__init__(*args, **kwargs)
