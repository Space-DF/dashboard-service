FROM python:3.10-alpine
ENV PYTHONUNBUFFERED=1

RUN apk add build-base libffi-dev curl
# Allows docker to cache installed dependencies between builds
COPY ./dashboard-service/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./django-common-utils django-common-utils
RUN pip install ../django-common-utils

# Adds our application code to the image
COPY ./dashboard-service dashboard-service

WORKDIR /dashboard-service

EXPOSE 80

ENV DJANGO_SETTINGS_MODULE="dashboard_service.settings"

RUN ["chmod", "+x", "./docker-entrypoint.sh"]

# Run the production server
ENTRYPOINT ["./docker-entrypoint.sh"]
