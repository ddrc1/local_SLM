FROM nvidia/cuda:12.6.3-runtime-ubuntu22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
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
CMD ["flask", "--app", "main.py", "run", "--host", "0.0.0.0"]