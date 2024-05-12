## this file will collect all packets and extract the wanted data
## **connect to server
import subprocess
from scapy.layers.inet import ICMP, TCP
from scapy.sendrecv import AsyncSniffer
from packet_filter import http_packet_filter, tracert_packet_filter, ftp_packet_filter
from help import site, ip
from ftpCommand import execute_ftp_command


#the captured packets will be saved here
captured_packets = []

# detele the existing data in captured packets
def deletePackets():
    captured_packets.clear()


# Append a packet to the list
def capture_packets(packet):
    captured_packets.append(packet)


#***************************************** http *********************************************************#
# execute the http command with the given site
def http_command():
    # clear cash command (must run as administrator)
    subprocess.Popen("ipconfig /flushdns", shell=True)

    deletePackets()
    sniff_thread = AsyncSniffer(prn=capture_packets, count=25)
    sniff_thread.start()

    # Execute your command (replace with your actual command)
    command_to_execute = f"curl http://{site}"
    subprocess.Popen(command_to_execute, shell=True).wait()

#******************************************** tracert ******************************************************#
#while executing the tracert command the computer will use the ICMPv4
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


# filter for tracert command sniffing
# doesn't take packets from the ICMPv6 protocol
def tracert_filter(packet):
    if ICMP in packet:
        if (packet[ICMP].type == 128 or packet[ICMP].type == 129):
            return False
        return True
    return False


# execute the tracert command
def tracert_command():
    deletePackets()
    sniff_thread = AsyncSniffer(prn=capture_packets, count=6, lfilter=tracert_filter)
    sniff_thread.start()

    # Execute your command (replace with your actual command)
    command_to_execute = f"tracert {ip}"
    subprocess.Popen(command_to_execute, shell=True).wait()


#******************************************* ftp *******************************************************#
# check if dst or src port is 21 (ftp port)
def ftp_filter(packet):
    if TCP in packet and (packet[TCP].sport == 21 or packet[TCP].dport == 21):
        return True
    return False

# execute the tracert command
def ftp_command():
    deletePackets()
    interface = "Software Loopback Interface 1"
    sniff_thread = AsyncSniffer(prn=capture_packets, count=6, lfilter=ftp_filter, iface=interface)
    sniff_thread.start()

    # Execute the command (run client server)
    execute_ftp_command()




#******************************************** general ******************************************************#

# Scapy sniffs from all the netwrk interface/
# But we can ask Scapy to sniff only on a specific interface
def sniff_packets(command):
    if command == "http":
        http_command()
        filtered_packets = http_packet_filter(captured_packets)
    elif command == "tracert":
        tracert_command()
        filtered_packets = tracert_packet_filter(captured_packets)
    elif command == "ftp":
        ftp_command()
        filtered_packets = ftp_packet_filter(captured_packets)
    #if command not recognized
    else:
        return "error: command not recognized"
    print("len filtered:",len(filtered_packets))
    print(type(filtered_packets))
    for obj in filtered_packets:
        print(type(obj))
    return filtered_packets


