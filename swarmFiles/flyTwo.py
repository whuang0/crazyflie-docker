#!/usr/bin/env python3

import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

# URIs for each Crazyflie
# Make sure these match the unique addresses assigned in the Bitcraze client!
URI1 = 'radio://0/80/2M/E7E7E7E701'
URI2 = 'radio://0/80/2M/E7E7E7E702'

def main():
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    # Optional scan to show available Crazyflies
    print("Scanning for Crazyflies...")
    available = cflib.crtp.scan_interfaces()
    print("Found:")
    for cf in available:
        print(f"  {cf[0]}")

    # Use SyncCrazyflie to connect to each
    with SyncCrazyflie(URI1, cf=Crazyflie(rw_cache='./cache')) as scf1, \
         SyncCrazyflie(URI2, cf=Crazyflie(rw_cache='./cache')) as scf2:

        print(f"Connected to {URI1} and {URI2}")

        hlc1 = scf1.cf.high_level_commander
        hlc2 = scf2.cf.high_level_commander

        # Take off to 1.0 m over 2.0 seconds
        hlc1.takeoff(target_height=1.0, duration=2.0)
        hlc2.takeoff(target_height=1.0, duration=2.0)

        time.sleep(3.0)  # Hover for 3 seconds at 1.0 m

        # Land each drone to 0.0 m over 2.0 seconds
        hlc1.land(target_height=0.0, duration=2.0)
        hlc2.land(target_height=0.0, duration=2.0)

        time.sleep(3.0)  # Wait a bit for them to land

        # Always stop the commander after flight
        hlc1.stop()
        hlc2.stop()

        print("Flight complete!")

if __name__ == "__main__":
    main()