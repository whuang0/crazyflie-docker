# Start from Ubuntu 22.04
FROM ubuntu:22.04

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

###############################################################################
# 1. System & ROS 2 installation
###############################################################################

# 1.1 Install system packages needed (curl, gnupg, lsb-release) + pip
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg2 \
    lsb-release \
    python3-pip \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# 1.2 Add ROS 2 apt repository & GPG key
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc \
    | gpg --dearmor \
    | tee /usr/share/keyrings/ros-archive-keyring.gpg > /dev/null

RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
  http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" \
  | tee /etc/apt/sources.list.d/ros2.list > /dev/null

# 1.3 Install ROS 2 Humble Desktop
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-humble-desktop \
    && rm -rf /var/lib/apt/lists/*

###############################################################################
# 2. Python libraries (pip-based)
###############################################################################

# cflib: Crazyflie Python library
# rowan, nicegui: used by Crazyswarm2 for GUI and quaternion math
# transforms3d: for coordinate transforms
RUN pip3 install --no-cache-dir \
    cflib \
    rowan \
    nicegui \
    transforms3d

###############################################################################
# 3. Clone & Build Crazyswarm2
###############################################################################

# Create a workspace
RUN mkdir -p /crazyswarm2_ws/src
WORKDIR /crazyswarm2_ws/src

# Clone the Crazyswarm2 repository (with submodules)
RUN git clone --recursive https://github.com/IMRCLab/crazyswarm2

# Switch shell to bash so that we can 'source' properly
SHELL ["/bin/bash", "-c"]

# Build the workspace using colcon
WORKDIR /crazyswarm2_ws
RUN source /opt/ros/humble/setup.bash && \
    colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release

###############################################################################
# 4. Final setup
###############################################################################

# Default to bash shell when the container starts
CMD ["bash"]