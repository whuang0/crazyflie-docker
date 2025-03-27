import time
import cflib.crtp
from cflib.crazyflie import Crazyflie

available_uris = []

# Define the voltage thresholds for battery percentage mapping
VOLTAGE_TO_PERCENTAGE = {
    (4.2, 100),  # Fully charged
    (3.7, 50),   # Mid-charge
    (3.4, 0),    # Low battery
}

def voltage_to_percentage(voltage):
    for threshold, percentage in VOLTAGE_TO_PERCENTAGE:
        if voltage >= threshold:
            return percentage
    return 0  # Return 0% if voltage is below the lowest threshold

def check_battery(uri):
    cf = Crazyflie()
    cf.open_link(uri)
    
    time.sleep(1)

    battery_voltage = cf.param.get_value("pm.vbat")
    battery_percentage = voltage_to_percentage(battery_voltage)
    print(f"Battery Voltage for {uri}: {battery_voltage} V")
    print(f"Battery Percentage for {uri}: {battery_percentage}%")
          
    cf.close_link()

def main():
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()
    # Scan for Crazyflies in range
    for a in range(0, 7):
        available = cflib.crtp.scan_interfaces(0xe7e7e7e700 + a)
        if len(available) > 0:
            print("Found Crazyflies:")
            for cf in available:
                available_uris.append(cf[0])
                print(available_uris)
    for uri in available_uris:
        print(f"\nChecking battery values for {uri}")
        check_battery(uri)

if __name__ == '__main__':
    main()
