# sessions/Dockerfile

FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# If sessions shares the same requirements file as authentication, reuse it.
# Otherwise adjust as needed.
COPY ../requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

# Expose a different port (or you can use the same if running on different hosts)
EXPOSE 8001

# Run gunicorn with the sessions service WSGI entry point.
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8001"]
