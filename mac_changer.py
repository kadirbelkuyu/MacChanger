import subprocess
import optparse
import random
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change it s MAC adress")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC adress. Generates a random Mac adress if it is empty")
    (options, arguments) =  parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    if not options.new_mac:
        options.new_mac = (':'.join(['%02X' % random.randrange(0,255) for i in range(0,6)]))
        print("[+] Random MAC Address created " + options.new_mac)
    return options

def mac_change(interface,new_mac):
    print("[+] Changing MAC adress for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_mac_adress(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode('utf-8')
    mac_search_result = re.search(r"\w\w\:\w\w\:\w\w\:\w\w\:\w\w\:\w\w", ifconfig_result)

    if mac_search_result:
        return mac_search_result.group(0)
    else:
        print("[-] Could not read MAC adress.")


options = get_arguments()
current_mac_adress = get_mac_adress(options.interface)
print("Current MAC adress = " + str(current_mac_adress))

mac_change(options.interface,options.new_mac)
current_mac_adress = get_mac_adress(options.interface)

if current_mac_adress == options.new_mac:
    print("[+] MAC adress was successfully changed to " + current_mac_adress)
else:
    print("[-] MAC adress did not get changed.")
