import cflib.crtp

def main():
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    # Scan for Crazyflies in range
    available = cflib.crtp.scan_interfaces()
    print("Found Crazyflies:")
    for cf in available:
        print(cf[0])

if __name__ == '__main__':
    main()