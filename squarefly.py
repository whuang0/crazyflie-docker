import logging
import sys
import time
from threading import Event

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper

# URI for the Crazyflie
URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

# Default flight height
DEFAULT_HEIGHT = 0.5

# Event to ensure the deck is attached
deck_attached_event = Event()

# Set up logging
logging.basicConfig(level=logging.ERROR)

# Function to ensure the Flow deck is attached
def param_deck_flow(_, value_str):
    value = int(value_str)
    print(value)
    if value:
        deck_attached_event.set()
        print('Deck is attached!')
    else:
        print('Deck is NOT attached!')

# Function to make the Crazyflie fly in a square pattern
def fly_square(scf, side_length=1):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        # Fly in a square: 4 sides, each side is side_length meters long
        for _ in range(4):
            mc.forward(side_length)  # Move forward by side_length meters
            time.sleep(0.5)
            mc.turn_left(90)  # Turn 90 degrees to the left
            time.sleep(0.5)

        mc.stop()  # Stop the movement at the end

if __name__ == '__main__':
    cflib.crtp.init_drivers()

    # Connect to the Crazyflie
    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        # Add callback to check Flow deck attachment
        scf.cf.param.add_update_callback(group='deck', name='bcFlow2', cb=param_deck_flow)
        time.sleep(1)

        # Wait for the Flow deck to be attached
        if not deck_attached_event.wait(timeout=5):
            print('No flow deck detected!')
            sys.exit(1)

        # Start the square flight pattern
        fly_square(scf)
