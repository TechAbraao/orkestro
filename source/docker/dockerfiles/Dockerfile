FROM python:3.10-alpine

WORKDIR /app

RUN apk add --no-cache \
    gcc \
    musl-dev \
    mariadb-connector-c-dev \
    pkgconfig \
    libffi-dev \
    python3-dev \
    build-base \
    postgresql-dev

COPY source/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY source/ .

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
