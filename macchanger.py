#!/usr/bin/env python

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface", help="Specify the interface to change it's MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="Specify the new MAC address")

    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify a MAC address, use --help for more info.")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig = subprocess.check_output(["ifconfig", interface])
    mac_regex = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig.decode('utf-8'))

    if mac_regex:
        return mac_regex.group(0)
    else:
        print("[-] Could not read MAC address.")


get_options = get_arguments()
current_mac = get_current_mac(get_options.interface)
print("Current MAC address is " + str(current_mac))

change_mac(get_options.interface, get_options.new_mac)

current_mac = get_current_mac(get_options.interface)
if current_mac == get_options.new_mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address did not get changed.")
