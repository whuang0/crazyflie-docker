import logging
import sys
import time
import os
from threading import Event, Thread, Barrier

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander

# Default flight height
DEFAULT_HEIGHT = 0.5

# Set up logging
logging.basicConfig(level=logging.ERROR)

def param_deck_flow(event, _, value_str):
    """Callback function to check if the deck is attached."""
    value = int(value_str)
    if value:
        event.set()
        print('Deck is attached!')
    else:
        print('Deck is NOT attached!')

def fly_to_coordinates(uri, coordinates, barrier):
    """Controls a Crazyflie to fly to given coordinates."""
    # Create a unique cache directory for each Crazyflie
    safe_uri = uri.replace(":", "_").replace("/", "_")
    cache_dir = f"./cache_{safe_uri}"

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    deck_attached_event = Event()  # Unique event for this drone

    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache=cache_dir)) as scf:
        scf.cf.param.add_update_callback(group='deck', name='bcFlow2', cb=lambda a, b: param_deck_flow(deck_attached_event, a, b))
        time.sleep(1)

        if not deck_attached_event.wait(timeout=5):
            print(f'No flow deck detected on {uri}! Skipping.')
            return

        print(f'[ID: {uri[-2:]}] Ready to fly!')

        # Synchronize with other drones before takeoff
        barrier.wait()

        with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
            time.sleep(3)
            for x, y in coordinates:
                print(f'[ID: {uri[-2:]}] Moving to ({x}, {y})')
                mc.move_distance(x, y, 0)
                time.sleep(5)
            mc.stop()

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
        sys.exit(1)

    print(f'Found Crazyflies: {available_uris}')

    # Get user input for coordinates
    try:
        num_points = int(input('Enter the number of waypoints: '))
        coordinates = []
        for i in range(num_points):
            x, y = map(float, input(f'Enter coordinates {i+1} (x y): ').split())
            coordinates.append((x, y))
    except ValueError:
        print('Invalid input. Please enter numeric values.')
        sys.exit(1)

    # Barrier to synchronize all drones before flight
    barrier = Barrier(len(available_uris))

    # Launch Crazyflies in parallel
    threads = []
    for uri in available_uris:
        thread = Thread(target=fly_to_coordinates, args=(uri, coordinates, barrier))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print('All Crazyflies have completed their flights.')

if __name__ == '__main__':
    main()