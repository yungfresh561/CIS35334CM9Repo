#!/usr/bin/env python3
#networkFileRW.py
#Derek Key
#June 30th 2025
#Update routers and switches;
#read equipment from a file, write updates & errors to file

##---->>>> Use a try/except clause to import the JSON module
try:
    import json
except ImportError:
    print("Error: JSON module could not be imported")
    exit()

##---->>>> Create file constants for the file names; file constants can be reused
## There are 2 files to read this program: equip_r.txt and equip_s.txt
## There are 2 files to write in this program: updated.txt and errors.txt
ROUTER_FILE = "equip_r.txt"
SWITCH_FILE = "equip_s.txt"
UPDATED_FILE = "updated.txt"
ERRORS_FILE = "errors.txt"

#prompt constants
UPDATE = "\nWhich device would you like to update "
QUIT = "(enter x to quit)? "
NEW_IP = "What is the new IP address (111.111.111.111) "
SORRY = "Sorry, that is not a valid IP address\n"

#function to get valid device
def getValidDevice(routers, switches):
    validDevice = False
    while not validDevice:
        #prompt for device to update
        device = input(UPDATE + QUIT).lower()
        if device in routers.keys():
            return device
        elif device in switches.keys():
            return device
        elif device == 'x':
            return device
        else:
            print("That device is not in the network inventory.")

#function to get valid IP address
def getValidIP(invalidIPCount, invalidIPAddresses):
    validIP = False
    while not validIP:
        ipAddress = input(NEW_IP)
        octets = ipAddress.split('.')
        
        # Check if we have exactly 4 octets
        if len(octets) != 4:
            invalidIPCount += 1
            invalidIPAddresses.append(ipAddress)
            print(SORRY)
            continue
            
        #print("octets", octets)
        valid_octets = True
        for byte in octets:
            try:
                byte_val = int(byte)
                if byte_val < 0 or byte_val > 255:
                    valid_octets = False
                    break
            except ValueError:
                valid_octets = False
                break
        
        if not valid_octets:
            invalidIPCount += 1
            invalidIPAddresses.append(ipAddress)
            print(SORRY)
        else:
            return ipAddress, invalidIPCount

def main():
    ##---->>>> open files here
    #dictionaries
    ##---->>>> read the routers and addresses into the router dictionary
    routers = {}
    try:
        with open(ROUTER_FILE, 'r') as router_file:
            routers = json.load(router_file)
    except FileNotFoundError:
        print(f"Warning: {ROUTER_FILE} not found. Using default router data.")
        # Default router data from equip_r.txt
        routers = {"router1":"10.10.10.1", "router2":"20.20.20.1", "router3":"30.30.30.1"}
    except json.JSONDecodeError:
        print(f"Error: {ROUTER_FILE} is not valid JSON format. Using default router data.")
        routers = {"router1":"10.10.10.1", "router2":"20.20.20.1", "router3":"30.30.30.1"}
    except Exception as e:
        print(f"Error reading {ROUTER_FILE}: {e}. Using default router data.")
        routers = {"router1":"10.10.10.1", "router2":"20.20.20.1", "router3":"30.30.30.1"}

    ##---->>>> read the switches and addresses into the switches dictionary
    switches = {}
    try:
        with open(SWITCH_FILE, 'r') as switch_file:
            switches = json.load(switch_file)
    except FileNotFoundError:
        print(f"Warning: {SWITCH_FILE} not found. Using default switch data.")
        # Default switch data from equip_s.txt
        switches = {"switch1":"10.10.10.2", "switch2":"10.10.10.3", "switch3":"10.10.10.4",
                   "switch4":"10.10.10.5", "switch5":"20.20.20.2", "switch6":"20.20.20.3",
                   "switch7":"30.30.30.2", "switch8":"30.30.30.3", "switch9":"30.30.30.4"}
    except json.JSONDecodeError:
        print(f"Error: {SWITCH_FILE} is not valid JSON format. Using default switch data.")
        switches = {"switch1":"10.10.10.2", "switch2":"10.10.10.3", "switch3":"10.10.10.4",
                   "switch4":"10.10.10.5", "switch5":"20.20.20.2", "switch6":"20.20.20.3",
                   "switch7":"30.30.30.2", "switch8":"30.30.30.3", "switch9":"30.30.30.4"}
    except Exception as e:
        print(f"Error reading {SWITCH_FILE}: {e}. Using default switch data.")
        switches = {"switch1":"10.10.10.2", "switch2":"10.10.10.3", "switch3":"10.10.10.4",
                   "switch4":"10.10.10.5", "switch5":"20.20.20.2", "switch6":"20.20.20.3",
                   "switch7":"30.30.30.2", "switch8":"30.30.30.3", "switch9":"30.30.30.4"}

    #the updated dictionary holds the device name and new ip address
    updated = {}
    #list of bad addresses entered by the user
    invalidIPAddresses = []
    #accumulator variables
    devicesUpdatedCount = 0
    invalidIPCount = 0
    #flags and sentinels
    quitNow = False
    validIP = False

    print("Network Equipment Inventory\n")
    print("\tequipment name\tIP address")
    for router, ipa in routers.items():
        print("\t" + router + "\t\t" + ipa)
    for switch, ipa in switches.items():
        print("\t" + switch + "\t\t" + ipa)

    while not quitNow:
        #function call to get valid device
        device = getValidDevice(routers, switches)
        if device == 'x':
            quitNow = True
            break

        #function call to get valid IP address
        #python lets you return two or more values at one time
        ipAddress, invalidIPCount = getValidIP(invalidIPCount, invalidIPAddresses)

        #update device
        if 'r' in device:
            #modify the value associated with the key
            routers[device] = ipAddress
            #print("routers", routers)
        else:
            switches[device] = ipAddress

        devicesUpdatedCount += 1
        #add the device and ipAddress to the dictionary
        updated[device] = ipAddress
        print(device, "was updated; the new IP address is", ipAddress)
        #loop back to the beginning

    #user finished updating devices
    print("\nSummary:")
    print()
    print("Number of devices updated:", devicesUpdatedCount)

    ##---->>>> write the updated equipment dictionary to a file using JSON
    try:
        with open(UPDATED_FILE, 'w') as updated_file:
            json.dump(updated, updated_file, indent=4)
        print("Updated equipment written to file 'updated.txt'")
    except Exception as e:
        print(f"Error writing to {UPDATED_FILE}: {e}")

    print()
    print("\nNumber of invalid addresses attempted:", invalidIPCount)

    ##---->>>> write the list of invalid addresses to a file using JSON
    try:
        with open(ERRORS_FILE, 'w') as errors_file:
            json.dump(invalidIPAddresses, errors_file, indent=4)
        print("List of invalid addresses written to file 'errors.txt'")
    except Exception as e:
        print(f"Error writing to {ERRORS_FILE}: {e}")

#top-level scope check
if __name__ == "__main__":
    main()
