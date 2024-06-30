from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField

from shipping_service.shipping.common import BaseModelMixin, PositiveDecimalField

MAX_TEXT_LENGTH = 255
DEFAULT_CURRENCY = 'EUR'
SUPPORTED_CURRENCY = ('EUR',)


class City(models.TextChoices):
    Berlin = "Berlin", _("Berlin")


class Country(models.TextChoices):
    Germany = "DE", "DE"


class Address(BaseModelMixin, models.Model):
    address_line_1 = models.CharField(max_length=MAX_TEXT_LENGTH)
    address_line_2 = models.CharField(max_length=MAX_TEXT_LENGTH, null=True, blank=True)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(
        max_length=MAX_TEXT_LENGTH,
        choices=City.choices,
        default=City.Berlin,
        db_index=True,
    )
    country_code = models.CharField(
        max_length=MAX_TEXT_LENGTH,
        choices=Country.choices,
        default=Country.Germany,
        db_index=True,
    )


class Package(BaseModelMixin, models.Model):
    dimension_x = PositiveDecimalField(help_text='dimension x in cm')
    dimension_y = PositiveDecimalField(help_text='dimension y in cm')
    dimension_z = PositiveDecimalField(help_text='dimension z in cm')
    weight = PositiveDecimalField(help_text='weight in grams')


class Carrier(models.TextChoices):
    dhl_express = "dhl-express", _("dhl-express")
    ups = "ups", _("ups")
    fedex = "fedex", _("fedex")


class Shipment(BaseModelMixin, models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_uq_code_type",
                fields=("number", "carrier"),
            )
        ]
        ordering = ("-created_at",)

    number = models.CharField(
        max_length=MAX_TEXT_LENGTH,
        db_index=True,
        help_text="aka tracking number",
    )
    date = models.DateTimeField(help_text="when the package was picked by the carrier")
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True)
    shipping_service_price = MoneyField(max_digits=14, decimal_places=2, default_currency=DEFAULT_CURRENCY)
    carrier = models.CharField(
        max_length=MAX_TEXT_LENGTH,
        choices=Carrier.choices,
        default=Carrier.dhl_express,
        db_index=True,
    )
