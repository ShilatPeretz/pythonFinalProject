from scapy.layers.inet import *
from version2.classes.HttpPacketsClass import HttpPacket
from version2.classes.TracertPacketClass import TracertPacket
from version2.classes.FtpPacketsClass import FtpPacket
from help import get_packet_show_output, site


#***************************************** http *********************************************************#
#tcp flags
tcp_flags = {
    "FIN": 0x01,
    "SYN": 0x02,
    "PSH": 0x08,
    "ACK": 0x10,
}

# identify each packet and sent it to the class to generate reduced packet
# DNS + HTTP + TCP
def http_packet_filter(captured_packets):
    filtered_packets = []
    for packet in captured_packets:
        show_output = get_packet_show_output(packet)
        # print(show_output)
        if site in show_output or "http" in show_output:
            filtered_packets.append(HttpPacket(packet))

    return filtered_packets




#***************************************** tracert *********************************************************#
icmp_types = {
# ICMPv4 types
    0: "Echo Reply",
    3: "Destination Unreachable",
    8: "Echo Request",
    11: "Time Exceeded",

# ICMPv6 types
    128: "Echo Request",
    129: "Echo Reply",

}


# tracert command packet filter
# takes only 1 packet of each hop
# tracert packets have maximum 30 hops
def tracert_packet_filter(captured_packets):
    # ttl counter
    ttl=1
    filtered_packets = []
    # counter for each hop 3 messages are sent we only take 1
    tmp = 1
    for i in range(len(captured_packets)):
        if (captured_packets[i][ICMP].type == 8) and captured_packets[i][IP].ttl == ttl:
            if (captured_packets[i+1][ICMP].type == 11 or captured_packets[i+1][ICMP].type == 0):
                filtered_packets.append(TracertPacket(captured_packets[i]))
                print(captured_packets[i].show())
                filtered_packets.append(TracertPacket(captured_packets[i+1]))

                print(captured_packets[i+1].show())
                print(captured_packets[i+1][ICMP].type)
                ttl+=1
                i+=1
            # an echo request was sent but there was no response because of "Request timed out"
            elif tmp == 3:
                # TODO: think of a way to add the time out
                filtered_packets.append(TracertPacket(captured_packets[i]))
                ttl+=1
                tmp-=2 # back to counting from 1
        tmp+=1

    print(len(filtered_packets))
    return filtered_packets


#***************************************** ftp *********************************************************#
# FTP + TCP packets
# unlike other functions here the packets recived are already filtered
# this function will only create class packets
def ftp_packet_filter(captured_packets):
    filtered_packets = []
    for packet in captured_packets:
        filtered_packets.append(FtpPacket(packet))
    print("filtered packet len: ")
    print(len(filtered_packets))
    return
