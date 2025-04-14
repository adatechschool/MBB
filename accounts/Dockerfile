# accounts\Dockerfile

FROM python:3.12-slim

# Set environment variable to prevent Python buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY ../requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the project files
COPY . /app/

# Expose the port on which the app will run
EXPOSE 8002

# Use gunicorn to serve the Django app. The DJANGO_SETTINGS_MODULE is loaded via environment.
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8002"]