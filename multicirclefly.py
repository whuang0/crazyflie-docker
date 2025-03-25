"""
GOAL: Fly multiple crazyflies in the same circle
# TODO: figure out where a certain drone is now - since URIs are constant, we can just organize by URI/ID when we put the drones down
# TODO: parameter for circle indicating that we are already at degree X in MotionCommander.circle_right?
"""
import logging
import time
from threading import Event, Thread, Barrier

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander


METERS_TO_FEET = 3.28084  # The tape grid is in feet


# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)


def circle_fly(uri: str, barrier: Barrier):
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)

    with SyncCrazyflie(uri) as scf:
        # We take off when the commander is created

        barrier.wait()
        
        time.sleep(0.1)
        barrier.reset()  # We need to use the barrier at each stage, so reset now

        with MotionCommander(scf) as mc:
            print('Taking off! [', uri[-2:], ']')
            time.sleep(1)

            # print('Moving up 0.2m')
            mc.up(0.2)
            # Wait a bit
            time.sleep(1)

            barrier.wait()  # Sync the circle

            print('Starting circle! [', uri[-2:], ']')
            mc.circle_right(2 / METERS_TO_FEET, velocity=0.5, angle_degrees=360)

            # We land when the MotionCommander goes out of scope
            print('Landing! [', uri[-2:], ']')


def main():
    cflib.crtp.init_drivers()

    # Scan for Crazyflies in range
    available_uris = []
    for a in range(0, 7):
        available = cflib.crtp.scan_interfaces(0xe7e7e7e700 + a)
        if available:
            available_uris.extend([cf[0] for cf in available])

    if not available_uris:
        print('No Crazyflies found!')
        exit(1)

    print(f'Found Crazyflies: {available_uris}')

    # Barrier to synchronize all drones before flight
    barrier = Barrier(len(available_uris))

    # Launch Crazyflies in parallel
    threads = []
    for uri in available_uris:
        thread = Thread(target=circle_fly, args=(uri, barrier))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print('All Crazyflies have completed their flights.')


if __name__ == '__main__':
    main()