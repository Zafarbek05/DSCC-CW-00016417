# Stage 1: Builder
FROM python:3.12-alpine AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache gcc musl-dev postgresql-dev

# Install dependencies and build wheels
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt python-decouple


# Stage 2: Final Production Image
FROM python:3.12-alpine

# Create a non-root user for security
RUN addgroup -S mygroup && adduser -S myuser -G mygroup

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV HOME=/home/myuser
ENV APP_HOME=/home/myuser/web

# Create static folder and give ownership to the non-root user
RUN mkdir -p $APP_HOME/staticfiles && chown myuser:mygroup $APP_HOME/staticfiles
WORKDIR $APP_HOME

# Install runtime dependencies for Postgres
RUN apk add --no-cache libpq

# Copy wheels and requirements from builder
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Install the wheels and delete the raw wheel files in the exact same layer
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir /wheels/* && \
    rm -rf /wheels /root/.cache

# Copy project files and set permissions
COPY --chown=myuser:mygroup . $APP_HOME

# Switch to the non-root user
USER myuser

# Expose the port Gunicorn will run on
EXPOSE 8000

# Start Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]