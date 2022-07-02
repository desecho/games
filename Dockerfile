FROM python:3.10-alpine

ARG REQUIREMENTS=requirements.txt

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY $REQUIREMENTS .

RUN apk add --no-cache --virtual .build-deps git gcc musl-dev libffi-dev openssl-dev python3-dev cargo && \
    apk add --no-cache mariadb-dev && \
    pip3 install --no-cache-dir -r $REQUIREMENTS && \
    apk del .build-deps && \
    rm $REQUIREMENTS

COPY src .

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "games_project.wsgi:application"]
