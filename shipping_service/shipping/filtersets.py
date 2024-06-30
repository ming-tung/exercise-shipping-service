from django_filters import rest_framework

from shipping_service.shipping.models import Shipment


class ShipmentFilterSet(rest_framework.FilterSet):
    shipping_service_price = rest_framework.RangeFilter(field_name="shipping_service_price")
    date = rest_framework.DateFromToRangeFilter(field_name='date')

    class Meta:
        model = Shipment
        fields = Shipment.model_fields()
