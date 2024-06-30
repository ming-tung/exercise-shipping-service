from collections import OrderedDict
from unittest.mock import patch

import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from shipping_service.shipping.cron import batch_create_shipments


@pytest.fixture
def client() -> APIClient:
    return APIClient(HTTP_ACCEPT='application/json; version=1.0')


@pytest.mark.django_db
class TestShipmentViewSetGET:
    url = reverse('shipping:shipment-list')

    def test_get_empty_list(self, client):
        response = client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'count': 0,
            'next': None,
            'previous': None,
            'results': [],
        }

    @pytest.mark.parametrize('request_data', ({}, {'page': 1}))
    def test_get_first_page(self, client, request_data, shipments_counts_101):
        response = client.get(self.url, data=request_data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 101
        assert response.data['next'] is not None
        assert response.data['previous'] is None
        assert len(response.data['results']) == 100

    def test_get_last_page(self, client, shipments_counts_101):
        response = client.get(self.url, data={'page': 2})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 101
        assert response.data['next'] is None
        assert response.data['previous'] is not None
        assert len(response.data['results']) == 1

    @pytest.mark.parametrize(
        'data, expected_count',
        (
            ({'carrier': 'dhl-express'}, 101),
            ({'shipping_service_price_max': 2.50}, 101),
            ({'shipping_service_price_min': 2.50}, 0),
            ({'date_before': '2024-06-20'}, 101),
            ({'date_after': '2024-06-20'}, 0),
            ({'date_before': '2024-06-20', 'carrier': 'dhl-express'}, 101),
            ({'date_before': '2024-06-20', 'carrier': 'ups'}, 0),
        ),
    )
    def test_filter(self, client, data, expected_count, shipments_counts_101):
        response = client.get(self.url, data=data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == expected_count


@pytest.mark.django_db
class TestShipmentViewSetPOST:
    url = reverse('shipping:shipment-list')

    def test_bad_request_empty_data(self, client):
        response = client.post(self.url, data=[{'unknown': 'asdf'}], format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert str(response.data[0]['number'][0]) == 'This field is required.'
        assert str(response.data[0]['date'][0]) == 'This field is required.'
        assert str(response.data[0]['address'][0]) == 'This field is required.'
        assert str(response.data[0]['package'][0]) == 'This field is required.'
        assert str(response.data[0]['shipping_service_price'][0]) == 'This field is required.'

    def test_post(self, client):
        data = [
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
        with patch.object(batch_create_shipments, 'delay') as mock_batch_create_shipment:
            response = client.post(self.url, data=data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert mock_batch_create_shipment.call_count == 1
        assert OrderedDict(mock_batch_create_shipment.call_args.args[0][0]) == OrderedDict(data[0])
