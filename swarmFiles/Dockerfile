#
# Dockerfile for Crazyswarm2 (Flow Deck only, no external MoCap)
# run: docker build -t crazyswarm2-flow .

# run container

# docker run -it --rm \
#   --net=host \
#   --privileged \
#   crazyswarm2-flow


# INSIDE CONTAINER:

# source /opt/ros/humble/setup.bash
# source /crazyswarm2_ws/install/setup.bash

# VERIFY PATH: 
# ros2 pkg list | grep crazyswarm2


#ros2 launch crazyswarm2 single_cf_hover_cflib.launch.py \
# swarm_config:=/path/to/your/crazyflie.yaml

FROM ubuntu:22.04

# Prevent interactive prompts during apt installs
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# --------------------------------------------------------------------------
# 1. Base system updates & prerequisites
# --------------------------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg2 \
    lsb-release \
    build-essential \
    git \
    python3-pip \
    # For USB and Boost libs:
    libusb-1.0-0-dev \
    libboost-program-options-dev \
    && rm -rf /var/lib/apt/lists/*

# --------------------------------------------------------------------------
# 2. Install ROS 2 Humble (desktop variant)
#    (If you want a lighter image, use ros-humble-ros-base instead)
# --------------------------------------------------------------------------
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc \
    | gpg --dearmor \
    | tee /usr/share/keyrings/ros-archive-keyring.gpg > /dev/null

RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
  http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" \
  | tee /etc/apt/sources.list.d/ros2.list > /dev/null

RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-humble-desktop \
    python3-colcon-common-extensions \
    # IMPORTANT: We skip ros-humble-motion-capture-tracking since no external MoCap
    && rm -rf /var/lib/apt/lists/*

# --------------------------------------------------------------------------
# 3. Python libraries for Crazyswarm2 (Flow Deck use)
# --------------------------------------------------------------------------
#   cflib        -> Crazyflie Python library
#   rowan        -> quaternion math
#   nicegui      -> UI components used by Crazyswarm2
#   transforms3d -> extra transformations
RUN pip3 install --no-cache-dir \
    cflib \
    rowan \
    nicegui \
    transforms3d

# --------------------------------------------------------------------------
# 4. Clone and build Crazyswarm2
# --------------------------------------------------------------------------
RUN mkdir -p /crazyswarm2_ws/src
WORKDIR /crazyswarm2_ws/src

# Clone the Crazyswarm2 repo (with submodules)
RUN git clone --recursive https://github.com/IMRCLab/crazyswarm2

# Switch shell to bash so 'source' works properly in Docker RUN commands
SHELL ["/bin/bash", "-c"]

WORKDIR /crazyswarm2_ws
RUN source /opt/ros/humble/setup.bash && \
    colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release

# --------------------------------------------------------------------------
# 5. (Optional) Copy in Crazyradio USB rules
# --------------------------------------------------------------------------
# COPY 99-crazyradio.rules /etc/udev/rules.d/99-crazyradio.rules
# RUN udevadm control --reload-rules && udevadm trigger

# By default, just drop to a bash shell
CMD ["bash"]