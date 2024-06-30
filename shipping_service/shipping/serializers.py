from rest_framework import serializers

from shipping_service.shipping.models import DEFAULT_CURRENCY, SUPPORTED_CURRENCY, Address, Package, Shipment


class AddressSerializer(serializers.ModelSerializer):
    address_line_2 = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Address
        fields = Address.model_fields()


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = Package.model_fields()


class ShipmentSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    package = PackageSerializer()

    # MoneyField is not supported properly by drf, so we need to add this `_currency`
    shipping_service_price_currency = serializers.ChoiceField(choices=SUPPORTED_CURRENCY, default=DEFAULT_CURRENCY)

    class Meta:
        model = Shipment
        fields = Shipment.model_fields()
