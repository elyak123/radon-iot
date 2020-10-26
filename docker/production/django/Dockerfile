FROM 3.8.6-slim-buster

RUN useradd --create-home appuser

USER appuser
ENV PYTHONUNBUFFERED 1

COPY ./requirements /requirements

COPY install-packages.sh .

RUN ./install-packages.sh

COPY . /app/radon

COPY ./docker/production/django/gunicorn.sh /app/gunicorn.sh
RUN sed -i 's/\r//' /app/gunicorn.sh

COPY ./docker/production/django/entrypoint.sh /app/entrypoint.sh
RUN sed -i 's/\r//' /app/entrypoint.sh

WORKDIR /app/radon

ENTRYPOINT ["app/entrypoint.sh"]
