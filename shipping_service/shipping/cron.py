import logging

from djmoney.money import Money

from celery import shared_task
from shipping_service.shipping.models import Address, Package, Shipment


@shared_task(name="batch_create_shipment")
def batch_create_shipments(shipments: list) -> int:
    logging.info(f'batch create shipments: {shipments}')
    # We could further slice the batch if it is big
    # We could consider to use bulk_create provided by django
    count_before = Shipment.objects.count()
    for shipment in shipments:
        address, _ = Address.objects.get_or_create(**shipment['address'])
        package, _ = Package.objects.get_or_create(**shipment['package'])
        shipping_service_price = Money(
            shipment['shipping_service_price'],
            shipment['shipping_service_price_currency'],
        )
        _shipment, _ = Shipment.objects.get_or_create(
            number=shipment['number'],
            date=shipment['date'],
            address=address,
            package=package,
            shipping_service_price=shipping_service_price,
            carrier=shipment['carrier'],
        )
    count_after = Shipment.objects.count()
    counts = count_after - count_before
    logging.info(f'{counts} shipments created')
    return counts
