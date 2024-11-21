FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-0 \
    libusb-1.0-0-dev \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Crazyflie Python library
RUN pip install --no-cache-dir cflib

# Copy the Crazyflie control script into the container
COPY circlefly.py /app/

# Default command to run the Crazyflie script
CMD ["python", "/app/circlefly.py"]
