from rest_framework.routers import DefaultRouter

from shipping_service.shipping import views


class BaseRouter(DefaultRouter):
    def __init__(self, *args, **kwargs):
        kwargs['trailing_slash'] = False
        super().__init__(*args, **kwargs)


router = BaseRouter()

router.register(
    'shipment',
    views.ShipmentViewSet,
    basename='shipment',
)
