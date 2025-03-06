import cflib.crtp


available_uris = []

def main():
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()
    # Scan for Crazyflies in range
    for a in range(0, 7):
        available = cflib.crtp.scan_interfaces(0xe7e7e7e700 + a)
        if (len(available) > 0):
            print("Found Crazyflies:")
            for cf in available:
                available_uris.append(cf[0])

if __name__ == '__main__':
    main()