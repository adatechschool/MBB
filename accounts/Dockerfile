# accounts\Dockerfile

FROM python:3.13-alpine AS builder

ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN apk add --no-cache \
    build-base \
    musl-dev \
    postgresql-dev

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip wheel --no-cache-dir -w /wheels -r requirements.txt

FROM python:3.13-alpine

ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN apk add --no-cache \
    libpq

COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt \
    && rm -rf /wheels

COPY ../configuration ./configuration
COPY . .

RUN addgroup -S app && adduser -S app -G app
USER app

EXPOSE 8002
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8002"]
