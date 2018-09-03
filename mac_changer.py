import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change it s MAC adress")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC adress")
    (options, arguments) =  parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    elif not options.new_mac:
        parser.error("[-] Please specify an mac, use --help for more info")
    return options

def mac_change(interface,new_mac):
    print("[+] Changing MAC adress for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_mac_adress(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
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

