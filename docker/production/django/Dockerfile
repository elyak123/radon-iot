FROM python:3.8.6-slim-buster

COPY docker/production/django/install_os_dependencies.sh .

RUN chmod +x /install_os_dependencies.sh

RUN ./install_os_dependencies.sh

RUN useradd --create-home appuser

COPY ./docker/production/django/gunicorn.sh /app/gunicorn.sh
RUN chown -R appuser /app/
RUN chmod 0700 /app/gunicorn.sh

COPY ./docker/production/django/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

USER appuser

ENV PYTHONUNBUFFERED 1

ENV VIRTUAL_ENV=/home/appuser/.virtualenvs
RUN python3 -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./requirements /requirements

COPY . /app/radon

RUN pip install wheel pip-tools && \
    pip-sync requirements/base.txt && \
    pip uninstall -y pip-tools

RUN sed -i 's/\r//' /app/gunicorn.sh

RUN sed -i 's/\r//' /app/entrypoint.sh

WORKDIR /app/radon

ENTRYPOINT ["/app/entrypoint.sh"]
