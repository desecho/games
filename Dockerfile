FROM python:3.11.0-alpine3.16

ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .

RUN apk add --no-cache --virtual .build-deps git gcc musl-dev libffi-dev openssl-dev python3-dev cargo && \
    apk add --no-cache mariadb-dev && \
    pip3 install --no-cache-dir uv==0.11.6 && \
    uv sync --no-dev --frozen && \
    apk del .build-deps && \
    rm uv.lock pyproject.toml

COPY src .

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "games_project.wsgi:application"]
