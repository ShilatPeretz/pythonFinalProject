import scapy.all as scapy
from scapy.layers.inet import *

class packet:
    def __init__(self, name, protocol, srcip, dstip, mac, port, payload, ttl):
        self.name = name
        self.protocol = protocol
        self.srcip = srcip
        self.dstip = dstip
        self.mac = mac
        self.port = port
        self.payload = payload
        self.ttl = ttl

    def process_packet(self, packet):
        self.srcip = packet[IP].src if IP in packet else None
        self.dstip = packet[IP].dst if IP in packet else None
        self.protocol = packet.proto if hasattr(packet,'proto') else None
        self.payload = str(packet)
