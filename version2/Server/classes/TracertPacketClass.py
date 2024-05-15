from scapy.layers.inet import *
from scapy.layers.inet6 import IPv6
from ..help import get_packet_show_output



class TracertPacket:
    icmp_types = {
        # ICMPv4 types
        0: "Echo Reply",
        3: "Destination Unreachable",
        8: "Echo Request",
        11: "Time Exceeded"
    }
    protocol_names = {
        1: "ICMP",
        6: "TCP",
        17: "UDP",
        # Add more mappings as needed
    }

    # init
    def __init__(self, packet):
        global show_output
        show_output = get_packet_show_output(packet)

        # packet data
        self.payload = show_output

        show_output = show_output.replace(" ", "")

        #self.protocol = packet.proto if hasattr(packet,'proto') else None
        if Ether in packet:
            # Access source and destination MAC addresses
            self.src_mac = packet[Ether].src
            self.dst_mac = packet[Ether].dst

        # protocol
        self.protocol = self.protocol_names.get(packet[IP].proto) if IP in packet else "none"

        # packet name
        p_type = packet[ICMP].type if ICMP in packet else "none"
        if (p_type == 8):
            self.name = "request"
        else:
            self.name = "reply"


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

        # icmp fields
        if (p_type==11):
            self.type = self.icmp_types.get(11)
        elif (p_type == 8):
            self.type = self.icmp_types.get(8)
        else:
            self.type=""



    # print the packet **only for developer**
    def print_packet(self):
        print("\n\n")
        if hasattr(self, 'name'):
            print("name: "+self.name)
        print("protocol "+self.protocol)
        print("src ip "+self.src_ip)
        print("dst ip " + self.dst_ip)
        print("src mac " + self.src_mac)
        print("dst mac " + self.dst_mac)
        print("ttl "+str(self.ttl))
        print("type "+self.type)

