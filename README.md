# Coding exercise
![CI](https://github.com/ming-tung/exercise-shipping-service/actions/workflows/ci.yaml/badge.svg?branch=main)
[![codecov](https://codecov.io/gh/ming-tung/exercise-shipping-service/graph/badge.svg?token=EMYPLW172T)](https://codecov.io/gh/ming-tung/exercise-shipping-service)

Shipping service - A dockerized API service powered by Django and Django Rest Framework

## System prerequisites
- docker, docker-compose
- [poetry](https://python-poetry.org/docs/#installation) if you want to run tests and linting locally

## Run tests and linting locally
Install dependencies using poetry:
```
poetry install
```

Run tests and linting:
```commandline
poetry run pytest
poetry run flake8 .
poetry run isort .
poetry run black .
```

## Run services: django app and postgres
```commandline
docker-compose up
```

### API
- The shipment endpoint is available at `http://localhost:8080/api/shipment`
- API authorization is out of scope here.

#### Example of POST request:
```commandline
curl -H "Content-Type: application/json" -X POST -d '[{"number": "test-post-1", "date": "2024-06-20T10:10:10Z", "address": {"address_line_1": "addr-100", "address_line_2": "", "postal_code": "12345", "city": "Berlin", "country_code": "DE"}, "package": {"dimension_x": "1.00", "dimension_y": "2.00", "dimension_z": "3.00", "weight": "5.00"}, "shipping_service_price_currency": "EUR", "shipping_service_price": "2.55", "carrier": "ups"}]' http://localhost:8080/api/shipment
```

#### Example of GET request with filter:
```commandline
curl http://localhost:8080/api/shipment?carrier=ups&date_before=2024-06-20
```

### API docs
API docs are available at [http://localhost:8080/docs/](http://localhost:8080/docs/).
The documentation is powered by drf_spectacular and generated based on Serializers.

## CI
Tests and checks are run in github actions - see`ci.yaml`.
The tests in CI runs against a sqlite database (see in [tests/settings.py](tests/settings.py)) rather than postgres simply for demonstration purpose. 

## Logging and Metrics
Use [opentelemetry](https://opentelemetry.io/) to enable tracing and monitoring.
