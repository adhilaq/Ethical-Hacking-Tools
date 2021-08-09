#!usr/bin/env python

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Enter interface")
    parser.add_option("-m", "--mac", dest="new_mac", help="Enter MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("Interface argument is missing")
    elif not options.new_mac:
        parser.error("MAC Address missing")

    return options


def change_mac(interface, new_mac):
    print("Changing MAC address for" + interface)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address:
        return mac_address.group(0)
    else:
        print("MAC Address not present")


option = get_arguments()
current_mac = get_current_mac(option.interface)
print("Current MAC:", str(current_mac))
change_mac(option.interface, option.new_mac)
current_mac = get_current_mac(option.interface)
if option.new_mac == current_mac:
    print("MAC Address changed to " + option.new_mac)
else:
    print("Error")