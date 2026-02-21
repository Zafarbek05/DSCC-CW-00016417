# Stage 1: Build dependencies
FROM python:3.12-alpine as builder
WORKDIR /app

# Install build dependencies required for psycopg2 and other packages
RUN apk update && apk add --no-cache postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt .
# Build wheels (compiled packages) instead of installing them directly
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Final ultra-small image
FROM python:3.12-alpine
WORKDIR /app

# Install only the runtime requirement for PostgreSQL
RUN apk update && apk add --no-cache libpq

# Create a non-root user for security
RUN adduser -D myuser
USER myuser

# Gunicorn needs to be in the PATH for the CMD to work
ENV PATH="/home/myuser/.local/bin:$PATH"

# Copy the compiled wheels from the builder stage and install them
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Copy your application code
COPY . .

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]