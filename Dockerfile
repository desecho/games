FROM python:3.10-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .

# Removing poetry manually because it doesn't work otherwise
RUN apk add --no-cache --virtual .build-deps git gcc musl-dev libffi-dev openssl-dev python3-dev cargo && \
    apk add --no-cache mariadb-dev && \
    pip3 install --no-cache-dir poetry==1.1.14 && \
    poetry config virtualenvs.create false --local && \
    poetry install --no-dev --no-root && \
    apk del .build-deps && \
    rm -rf /usr/local/lib/python3.10/site-packages/poetry && \
    rm poetry.toml poetry.lock pyproject.toml

COPY src .

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "games_project.wsgi:application"]
