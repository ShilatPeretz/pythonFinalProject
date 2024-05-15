from scapy.layers.inet import *
from scapy.layers.inet6 import IPv6
from ..help import get_packet_show_output


class FtpPacket:
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

        #packet data
        self.payload = show_output

        show_output = show_output.replace(" ","")

        # protocol
        self.protocol = self.protocol_names.get(packet[IP].proto) if IP in packet else "none"

        # default name if tcp packet
        self.name = "tcp"

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
            self.name = "ftp"
            self.raw = show_output.split("load=")[1]

        if TCP in packet:
            # Access source and destination ports for TCP
            self.src_port = packet[TCP].sport
            self.dst_port = packet[TCP].dport

            flag = show_output.split("TCP")[1].split("flags=")[1].split("\n")[0]
            self.flag = self.flags.get(flag)


        ##print the data collected
        # self.print_packet()

    def print_packet(self):
        print("\n\n")
        if hasattr(self, 'name'):
            print("name: "+self.name)
        if hasattr(self, 'flag'):
            print("tcp flag: "+str(self.flag))
        print("protocol "+self.protocol)
        print("src ip "+self.src_ip)
        print("dst ip " + self.dst_ip)
        print(f"src port { self.src_port}")
        print(f"dst port {self.dst_port}")
        if hasattr(self, 'raw'):
            print("raw: "+str(self.raw))

        print(f"\n\n { self.payload} ")






