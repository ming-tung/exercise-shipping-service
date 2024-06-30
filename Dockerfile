FROM python:3.12-slim as base

ENV PYTHONUNBUFFERED TRUE

WORKDIR /src
COPY poetry.lock pyproject.toml /src/
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get -y update && apt-get -y install curl && \
    useradd -u 1000 celery_user
RUN pip3 install poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction

COPY . /src

ENV PORT 8080

CMD python manage.py check; \
 python manage.py migrate --no-input; \
 python manage.py collectstatic --no-input; \
 exec opentelemetry-instrument gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 -c gunicorn.config.py shipping_service.wsgi
