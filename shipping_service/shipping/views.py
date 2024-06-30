from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from shipping_service.shipping.cron import batch_create_shipments
from shipping_service.shipping.filtersets import ShipmentFilterSet
from shipping_service.shipping.models import Shipment
from shipping_service.shipping.serializers import ShipmentSerializer


class ShipmentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ShipmentSerializer
    filterset_class = ShipmentFilterSet
    queryset = Shipment.objects
    lookup_field = 'uuid'

    @extend_schema(
        summary="Create shipment data",
        request=ShipmentSerializer(many=True),
        responses={201: OpenApiResponse(response=ShipmentSerializer(many=True))},
    )
    def create(self, request, *args, **kwargs):
        # We may want to consider the size of the list. If needed, to reject the request.
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        batch_create_shipments.delay(serializer.data)
        headers = self.get_success_headers(serializer.data)
        return Response({}, status=status.HTTP_201_CREATED, headers=headers)

    @extend_schema(
        summary="List shipment data",
        responses={200: OpenApiResponse(response=ShipmentSerializer)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
