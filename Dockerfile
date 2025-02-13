# Start from official ROS 2 Humble image
FROM ros:humble

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libboost-program-options-dev \
    libusb-1.0-0-dev \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python libraries needed
RUN pip3 install --no-cache-dir \
    cflib \
    rowan \
    nicegui \
    transforms3d

# Create a workspace and clone Crazyswarm2
RUN mkdir -p /crazyswarm2_ws/src
WORKDIR /crazyswarm2_ws/src
RUN git clone --recursive https://github.com/IMRCLab/crazyswarm2

# Build the workspace
WORKDIR /crazyswarm2_ws
SHELL ["/bin/bash", "-c"]
RUN source /opt/ros/humble/setup.bash && \
    colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release

# Copy your test script into the container
WORKDIR /app
COPY test_two_drones.py /app/test_two_drones.py

# (Optional) If you want to run the script at build time:
# This will fail unless you have USB hardware accessible during 'docker build'.
RUN python3 /app/test_two_drones.py

# Default to bash at runtime
CMD ["bash"]