# this ia a test file to check the scapySniff file
from scapysniff import sniff_packets
from classes.packetsClass import Packet

filtered_packets = sniff_packets("http")
for packet in filtered_packets:
    packet.print_packet()