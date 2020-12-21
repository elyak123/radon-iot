FROM python:3.8.6-alpine3.12 as builder

ENV PYTHONUNBUFFERED 1

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"
COPY ./requirements /requirements
RUN apk add --quiet --no-cache --virtual .build-deps \
    build-base gcc musl-dev libffi-dev postgresql-dev git \
      && pip install -q pip-tools==5.4.0 \
      && pip-sync -q requirements/production.txt \
      && pip uninstall -y pip-tools \
      && find /usr/local \
            \( -type d -a -name test -o -name tests \) \
            -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
            -exec rm -rf '{}' + \
      && runDeps="$( \
            scanelf --needed --nobanner --recursive /usr/local \
                     | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                     | sort -u \
                     | xargs -r apk info --installed \
                     | sort -u \
      )" \
      && apk add --virtual .rundeps $runDeps \
      && apk del --quiet .build-deps

FROM python:3.8.6-alpine3.12

ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache --virtual .build-deps \
    build-base bash gcc musl-dev libpq geos gdal proj \
      && find /usr/local \
            \( -type d -a -name test -o -name tests \) \
            -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
            -exec rm -rf '{}' + \
      && runDeps="$( \
            scanelf --needed --nobanner --recursive /usr/local \
                     | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                     | sort -u \
                     | xargs -r apk info --installed \
                     | sort -u \
      )" \
      && apk add --virtual .rundeps $runDeps \
      && apk del .build-deps

RUN addgroup -S appuser && adduser -S appuser -G appuser

COPY --from=builder /opt/venv /opt/venv

COPY --from=builder /app /app

COPY ./docker/production/django/gunicorn.sh /app/gunicorn.sh

COPY ./docker/production/django/entrypoint.sh /app/entrypoint.sh

RUN sed -i 's/\r//' /app/gunicorn.sh && \
    sed -i 's/\r//' /app/entrypoint.sh && \
    chown -R appuser:appuser /app/ && chmod -R 0700 /app/ && \
    chmod +x /app/entrypoint.sh

USER appuser

COPY . /app/radon

WORKDIR /app/radon

ENTRYPOINT ["/app/entrypoint.sh"]
