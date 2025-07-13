FROM python:3.13-alpine3.22

# Upgrade system packages and install dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy the application
COPY . /app

# Set the working directory
WORKDIR /app

# Install the application
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
EXPOSE 5000
CMD ["gunicorn", "-w", "-b", "0.0.0.0:5000", "main:app"]