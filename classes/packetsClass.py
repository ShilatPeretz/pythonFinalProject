import json

import scapy.all as scapy
from scapy.layers.dns import DNS
from scapy.layers.inet import *
from scapy.layers.inet6 import IPv6
from scapy.packet import Raw
from Server.help import get_packet_show_output


class Packet:
    protocol_names = {
        1: "ICMP",
        6: "TCP",
        17: "UDP",
        # Add more mappings as needed
    }
    flags = {
        'S': "SYN",
        'SA':"SYN-ACK",
        'A':'ACK',
        'PA':'PSH-ACK',
        'FA':'FIN-ACK'
    }
    def __init__(self, packet):
        global show_output
        show_output = get_packet_show_output(packet)
        show_output = show_output.replace(" ","")

        #self.protocol = packet.proto if hasattr(packet,'proto') else None
        if Ether in packet:
            # Access source and destination MAC addresses
            self.src_mac = packet[Ether].src
            self.dst_mac = packet[Ether].dst

        # protocol
        self.protocol = self.protocol_names.get(packet[IP].proto) if IP in packet else "none"

        if "DNS" in show_output:
            self.name = "DNS"
        elif "GET/HTTP" in show_output:
            self.name = "get - HTTP"
        elif "HTTP" in show_output:
            self.name = "HTTP"
        elif "TCP" in show_output:
            self.name = "TCP"
        else:
            "no name"

        # Assuming 'packet' is the IPv6 packet captured or generated using Scapy
        if IPv6 in packet:
            # Access source and destination IPv6 addresses
            self.src_ip = packet[IPv6].src
            self.dst_ip = packet[IPv6].dst

        elif IP in packet:
            # Access source and destination IP addresses
            self.src_ip = packet[IP].src
            self.dst_ip = packet[IP].dst
            #ttl - **doesn't apear if using IPv6
            self.ttl = packet[IP].ttl

        if "Raw" in show_output:
            self.raw = show_output.split("load=")[1]

        if TCP in packet:
            # Access source and destination ports for TCP
            self.src_port = packet[TCP].sport
            self.dst_port = packet[TCP].dport

            flag = show_output.split("flags=")[1].split("\n")[0]
            self.flag = self.flags.get(flag)

        elif UDP in packet:
            # Access source and destination ports for UDP
            self.src_port = packet[UDP].sport
            self.dst_port = packet[UDP].dport

        #packet data
        self.payload = show_output

        ##print the data collected
        #self.print_packet()

    def print_packet(self):
        print("\n\n")
        if hasattr(self, 'name'):
            print("name: "+self.name)
        if hasattr(self, 'flag'):
            print("tcp flag: "+str(self.flag))
        print("protocol "+self.protocol)
        print("src ip "+self.src_ip)
        print("dst ip " + self.dst_ip)
        print("src mac " + self.src_mac)
        print("dst mac " + self.dst_mac)
        print(f"src port { self.src_port}")
        print(f"dst port {self.dst_port}")
        if hasattr(self, 'raw'):
            print("raw: "+str(self.raw))


    # def set_dns_packet(self,packet):
    #     #add the query/response
    #     tmp = packet.show()
    #
    #     return 0
    #
    # def set_http_packet(self):
    #     #add request method + requesr or answer
    #     #collect the syn, ack, syn ack (three way handshake)
    #     return 0
    #
    # def set_traceroute_packet(self):
    #     return 0

    #ARP? - in tracerote
    #DHCP




