#!usr/bin/env python3

import scapy.all as scapy
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP/IP Range")
    options = parser.parse_args()
    return options


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_broadcast, timeout=1, verbose=False)[0]
    client_list = []
    for element in answered_list:
        client_list.append({"ip": element[1].psrc, "mac": element[1].hwsrc})
    return client_list


def print_result(result):
    print("IP\t\t\tMAC Address\n------------------------------")
    for client in result:
        print(client["ip"] + "\t\t" + client["mac"])


options = get_arguments()
result = scan(options.target)
print_result(result)
