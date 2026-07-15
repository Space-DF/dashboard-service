FROM python:3.10-alpine AS builder

ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache \
    build-base \
    libffi-dev \
    git

WORKDIR /install

# install private repo from local directory
COPY django-common-utils /install/django-common-utils
RUN pip install --no-cache-dir --prefix=/install /install/django-common-utils

# install python requirements
COPY dashboard-service/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.10-alpine

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE="dashboard_service.settings"

RUN apk add --no-cache \
    curl \
    libffi

WORKDIR /app

# copy installed python packages
COPY --from=builder /install /usr/local
COPY dashboard-service .

RUN ["chmod", "+x", "./docker-entrypoint.sh"]

# Run the production server
ENTRYPOINT ["./docker-entrypoint.sh"]
