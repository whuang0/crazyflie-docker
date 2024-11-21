# crazyflie

This repository contains flight scripts and a Docker container to run the script(s) for the Crazyflie 2.1+ Drone

To test the scripts:

    Verify usb path of Crazyflie dongle using terminal command:
    lsusb

    Should see something like this listed:
    Bus 003 Device 017: ID 1915:7777 Nordic Semiconductor ASA Bitcraze Crazyradio (PA) dongle


    Use Bus and Device number for the docker build and run command below

    docker build -t crazyflie-runner .
    docker run -it --rm --device=/dev/bus/usb/003/017 crazyflie-runner


If you want to test your own flight script ensure to change the Docker file respectively here before building the Docker:

    # Copy the Crazyflie control script into the container
    COPY circlefly.py /app/

    # Default command to run the Crazyflie script
    CMD ["python", "/app/circlefly.py"]