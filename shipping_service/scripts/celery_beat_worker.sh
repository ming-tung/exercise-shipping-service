#!/bin/sh
set -x
celery -A shipping_service.celery worker --beat --loglevel=info --uid 1000
