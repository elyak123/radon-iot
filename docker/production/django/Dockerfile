FROM python:3.8.6-slim-buster

COPY docker/production/django/install_os_dependencies.sh .

RUN chmod +x /install_os_dependencies.sh

RUN ./install_os_dependencies.sh

RUN useradd --create-home appuser

COPY ./requirements /requirements

COPY . /app/radon

COPY ./docker/production/django/gunicorn.sh /app/gunicorn.sh
RUN chown -R appuser:appuser /app/ && chmod -R 0700 /app/

COPY ./docker/production/django/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

USER appuser

ENV PYTHONUNBUFFERED 1

ENV VIRTUAL_ENV=/home/appuser/.virtualenvs

RUN python3 -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install wheel pip-tools  -q && \
    pip-sync requirements/production.txt -q && \
    pip uninstall -y pip-tools -q

RUN sed -i 's/\r//' /app/gunicorn.sh

RUN sed -i 's/\r//' /app/entrypoint.sh

WORKDIR /app/radon

ENTRYPOINT ["/app/entrypoint.sh"]
