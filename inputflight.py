import logging
import sys
import time
from threading import Event

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander

# Default flight height
DEFAULT_HEIGHT = 0.5

# Event to ensure the deck is attached
deck_attached_event = Event()

# Set up logging
logging.basicConfig(level=logging.ERROR)

def param_deck_flow(_, value_str):
    value = int(value_str)
    if value:
        deck_attached_event.set()
        print('Deck is attached!')
    else:
        print('Deck is NOT attached!')

def fly_to_coordinates(scf, coordinates):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        for x, y in coordinates:
            print(f'Moving to ({x}, {y})')
            mc.move_distance(x, y, 0)
            time.sleep(1)
        mc.stop()

if __name__ == '__main__':
    cflib.crtp.init_drivers()
    available = cflib.crtp.scan_interfaces()
    if not available:
        print('No Crazyflies found!')
        sys.exit(1)

    URI = available[0][0]
    print(f'Connecting to Crazyflie at URI: {URI}')

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        scf.cf.param.add_update_callback(group='deck', name='bcFlow2', cb=param_deck_flow)
        time.sleep(1)

        if not deck_attached_event.wait(timeout=5):
            print('No flow deck detected!')
            sys.exit(1)

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

        # Fly to inputted coordinates
        fly_to_coordinates(scf, coordinates)
