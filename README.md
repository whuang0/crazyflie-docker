# crazyflie

This repository contains a Dockerfile to run test python flight script(s) for the Crazyflie 2.1+ Drone

To test the scripts:

    Verify usb path of Crazyflie dongle using terminal command:

        lsusb

    Example path:
        
        Bus 003 Device 017: ID 1915:7777 Nordic Semiconductor ASA Bitcraze Crazyradio (PA) dongle


    Use Bus and Device number for the docker run command below:

        docker build -t crazyflie-runner .
        docker run -it --rm --device=/dev/bus/usb/003/017 crazyflie-runner


To test own flight script, prior to running docker build/run commands change python script in Dockerfile here:

    # Copy the Crazyflie control script into the container
    COPY circlefly.py /app/

    # Default command to run the Crazyflie script
    CMD ["python", "/app/circlefly.py"]
