import pytest
from djmoney.money import Money

from shipping_service.shipping.cron import batch_create_shipments
from shipping_service.shipping.models import Shipment


@pytest.mark.django_db
class TestBatchCreateShipments:
    def test_batch_create_shipments(self):
        shipments = [
            {
                "number": "test-post-1",
                "date": "2024-06-20T10:10:10Z",
                "address": {
                    "address_line_1": "addr-100",
                    "address_line_2": '',
                    "postal_code": "12345",
                    "city": "Berlin",
                    "country_code": "DE",
                },
                "package": {
                    "dimension_x": "1.00",
                    "dimension_y": "2.00",
                    "dimension_z": "3.00",
                    "weight": "5.00",
                },
                "shipping_service_price_currency": "EUR",
                "shipping_service_price": "2.55",
                "carrier": "ups",
            }
        ]

        count = batch_create_shipments(shipments)

        assert count == 1
        shipment = Shipment.objects.first()
        assert shipment.number == "test-post-1"
        assert str(shipment.date) == '2024-06-20 10:10:10+00:00'
        assert shipment.address.address_line_1 == 'addr-100'
        assert shipment.address.address_line_2 == ''
        assert shipment.address.postal_code == '12345'
        assert shipment.address.city == 'Berlin'
        assert shipment.address.country_code == 'DE'
        assert shipment.package.dimension_x == 1
        assert shipment.package.dimension_y == 2
        assert shipment.package.dimension_z == 3
        assert shipment.package.weight == 5
        assert shipment.shipping_service_price == Money(2.55, 'EUR')
        assert shipment.carrier == 'ups'
