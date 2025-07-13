FROM python:3.13-alpine3.22

# Upgrade system packages and install dependencies
RUN apk add --no-cache \
    build-base \
    libffi-dev \
    gcc \
    musl-dev \
    linux-headers

# Copy the application
COPY . /app

# Set the working directory
WORKDIR /app

# Install the application
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]