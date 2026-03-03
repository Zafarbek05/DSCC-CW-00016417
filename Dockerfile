# Stage 1: Builder
FROM python:3.12-alpine AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies for psycopg2 (Postgres)
RUN apk add --no-cache gcc musl-dev postgresql-dev

# Install dependencies and build wheels
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir python-decouple && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# Stage 2: Final Production Image
FROM python:3.12-alpine

# Create a non-root user for security (Requirement for 76%+ grade)
RUN addgroup -S mygroup && adduser -S myuser -G mygroup

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV HOME=/home/myuser
ENV APP_HOME=/home/myuser/web

RUN mkdir -p $APP_HOME/staticfiles
WORKDIR $APP_HOME

# Install runtime dependencies for Postgres
RUN apk add --no-cache libpq

# Copy wheels and requirements from builder
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Install the wheels
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir python-decouple && \
    pip install --no-cache-dir /wheels/*

# Copy the rest of the project files
COPY . $APP_HOME

# Fix permissions for the non-root user
RUN chown -R myuser:mygroup $APP_HOME

# Switch to the non-root user
USER myuser

# Expose the port Gunicorn will run on
EXPOSE 8000

# Start Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]