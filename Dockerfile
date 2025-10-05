# Base stage with Python Alpine image
FROM python:3.10-alpine AS base

# Builder stage for installing dependencies
FROM base AS builder
COPY requirements.txt /requirements.txt
RUN pip install --user -r /requirements.txt

# Final stage for running the application
FROM base

# Install Cairo and dependencies with DejaVu fonts for proper Unicode and italic support
RUN apk add --no-cache cairo cairo-dev ttf-dejavu fontconfig

COPY --from=builder /root/.local /root/.local
COPY src /app
WORKDIR /app

# Expose port
ENV PORT=8080
EXPOSE 8080

# Correct PATH environment variable
ENV PATH=/root/.local/bin:$PATH

# Command to run the Flask application with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "--worker-tmp-dir", "/dev/shm", "wsgi:app"]
