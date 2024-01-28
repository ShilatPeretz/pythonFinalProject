from scapy.layers.inet import *
from version1.classes.packetsClass import Packet
from help import get_packet_show_output, site


tcp_flags = {
    "FIN": 0x01,
    "SYN": 0x02,
    "PSH": 0x08,
    "ACK": 0x10,
}

#identify each packet and sent it to the class to generate reduced packet
#DNS + HTTP + TCP
def http_packet_filter(captured_packets):
    filtered_packets = []
    for packet in captured_packets:
        show_output = get_packet_show_output(packet)
        # print(show_output)
        if site in show_output or "http" in show_output:
            filtered_packets.append(Packet(packet))

    return filtered_packets


