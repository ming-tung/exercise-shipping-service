from djmoney.money import Money
from pytest import fixture

from shipping_service.shipping.models import Address, Carrier, City, Country, Package, Shipment


@fixture
def shipments_counts_101():
    for i in range(101):
        address = Address.objects.create(
            address_line_1=f'addr-{i}',
            postal_code='12345',
            city=City.Berlin,
            country_code=Country.Germany,
        )
        package = Package.objects.create(dimension_x=1, dimension_y=2, dimension_z=3, weight=4)
        Shipment.objects.create(
            number=f'test-{i}',
            date='2024-06-19T10:10:10Z',
            address=address,
            package=package,
            shipping_service_price=Money(1.55, 'EUR'),
            carrier=Carrier.dhl_express,
        )
