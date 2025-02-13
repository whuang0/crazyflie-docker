# TO RUN THIS DOCKERFILE:
# docker build -t crazyswarm2-flow .
# docker run -it --rm --net=host --privileged crazyswarm2-flow

# Start from the official ROS 2 Humble image
FROM ros:humble

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Install apt-based dependencies:
#  - libboost-program-options-dev (used by Crazyswarm2)
#  - libusb-1.0-0-dev (USB access for Crazyradio)
#  - build-essential, git (to build from source)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libboost-program-options-dev \
    libusb-1.0-0-dev \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python libraries for onboard flow usage
#  - cflib (Crazyflie Python library)
#  - rowan (quaternion math)
#  - nicegui (used by Crazyswarm2 for GUI)
#  - transforms3d (spatial transforms)
RUN pip3 install --no-cache-dir \
    cflib \
    rowan \
    nicegui \
    transforms3d

# Create a ROS workspace and clone Crazyswarm2
RUN mkdir -p /crazyswarm2_ws/src
WORKDIR /crazyswarm2_ws/src
RUN git clone --recursive https://github.com/IMRCLab/crazyswarm2

# Build the workspace using colcon
WORKDIR /crazyswarm2_ws
SHELL ["/bin/bash", "-c"]
RUN source /opt/ros/humble/setup.bash && \
    colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release

# (Optional) Copy in the Crazyradio udev rules file if you want it inside the container.
# Typically, it's easier to install on your host OS.
# COPY 99-crazyradio.rules /etc/udev/rules.d/99-crazyradio.rules
# RUN udevadm control --reload-rules && udevadm trigger

# Default command: just drop into bash.
CMD ["bash"]