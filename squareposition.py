import logging
import sys
import time
from threading import Event

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

# Default flight height
DEFAULT_HEIGHT = 0.3

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
def fly_square(scf):
    commander = scf.cf.high_level_commander

<<<<<<< HEAD
=======
    # time.sleep(5)

>>>>>>> 2d01036 (Updated Script for x, y coordinate testing with MotionCommander Class)
    # Take off to the default height
    commander.takeoff(DEFAULT_HEIGHT, 5)
    time.sleep(6)

    do_land = False

    while not do_land:

        input_from_user = input("Where to next? (X, Y, Z)\n")

        if (input_from_user == "land"):
            do_land = True
            continue
           

        points = input_from_user.split(" ")
        numbers = []

        print(f"number of points: {len(points)}")

        for point in points:
            numbers.append(float(point))
        if (len(numbers) == 2):
            numbers.append(DEFAULT_HEIGHT)
        print(f"Flying to X={numbers[0]}, Y={numbers[1]}, Z={numbers[2]}")

        

        commander.go_to(numbers[0], numbers[1], numbers[2], 0, 3.0)
        time.sleep(4)



    # Land after completing the square
    commander.land(0.0, 2.0)
    time.sleep(3)

if __name__ == '__main__':
    cflib.crtp.init_drivers()

    # Scan for available Crazyflie interfaces
    available = cflib.crtp.scan_interfaces()
    if not available:
        print('No Crazyflies found!')
        sys.exit(1)

    # Automatically select the first available URI
    URI = available[0][0]
    print(f'Connecting to Crazyflie at URI: {URI}')

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
