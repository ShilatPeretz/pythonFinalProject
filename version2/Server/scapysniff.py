## this file will collect all packets and extract the wanted data
## **connect to server
import subprocess
import threading

from scapy.layers.dns import DNS
from scapy.layers.inet import ICMP, TCP
from scapy.sendrecv import AsyncSniffer
from ftpCommand import execute_ftp_command

from classes.HttpPacketsClass import HttpPacket
from classes.TracertPacketClass import TracertPacket
from classes.FtpPacketsClass import FtpPacket


#the captured packets will be saved here
captured_packets = []

# detele the existing data in captured packets
def deletePackets():
    captured_packets.clear()


# Append a packet to the list
def capture_packets(packet):
    captured_packets.append(packet)


#***************************************** http *********************************************************#

# filter for http packets
# search DNS packets or port=80
def http_filter(packet):
    if DNS in packet:
        return True
    if TCP in packet and (packet[TCP].sport == 80 or packet[TCP].dport == 80):
        return True
    return False
# execute the http command with the given site
# Define a lock
http_lock = threading.Lock()

def http_command(site):
    # Acquire the lock before executing the function
    with http_lock:
        # clear cache command (must run as administrator)
        subprocess.Popen("ipconfig /flushdns", shell=True)

        deletePackets()
        sniff_thread = AsyncSniffer(prn=capture_packets, count=25, lfilter=http_filter)
        sniff_thread.start()

        # Execute your command (replace with your actual command)
        command_to_execute = f"curl http://{site}"
        subprocess.Popen(command_to_execute, shell=True).wait()


def create_http_packets(packets, site):
    http_packet_arr = []
    for p in packets:
        tmp = HttpPacket(p)
        if "DNS" in tmp.payload and site not in tmp.payload:
            continue
        http_packet_arr.append(tmp)
    return http_packet_arr
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
tracert_lock = threading.Lock()

def tracert_command(ip):
    # Acquire the lock before executing the function
    with tracert_lock:
        deletePackets()
        sniff_thread = AsyncSniffer(prn=capture_packets, count=250, lfilter=tracert_filter)
        sniff_thread.start()

        # Execute your command (replace with your actual command)
        command_to_execute = f"tracert {ip}"
        subprocess.Popen(command_to_execute, shell=True).wait()


def create_tracert_packets(packets):
    tracert_packet_arr = []
    for p in packets:
        tracert_packet_arr.append(TracertPacket(p))
    return tracert_packet_arr

#******************************************* ftp *******************************************************#
# check if dst or src port is 21 (ftp port)
def ftp_filter(packet):
    if TCP in packet and (packet[TCP].sport == 21 or packet[TCP].dport == 21):
        return True
    return False

# execute the tracert command
# Define a lock
ftp_lock = threading.Lock()

def ftp_command():
    # Acquire the lock before executing the function
    with ftp_lock:
        deletePackets()
        interface = "Software Loopback Interface 1"
        sniff_thread = AsyncSniffer(prn=capture_packets, count=100, lfilter=ftp_filter, iface=interface)
        sniff_thread.start()

        # Execute the command (run client server)
        execute_ftp_command()

def create_ftp_packets(packets):
    ftp_packet_arr = []
    for p in packets:
        ftp_packet_arr.append(FtpPacket(p))
    return ftp_packet_arr


#******************************************** general ******************************************************#

# Scapy sniffs from all the netwrk interface/
# But we can ask Scapy to sniff only on a specific interface
def sniff_packets(command):
    filtered_packets = []
    print("data: ",command)
    protocol, protocol_info = command.split(":")
    if protocol == "http":
        http_command(protocol_info)
        filtered_packets = create_http_packets(captured_packets, protocol_info)
    elif protocol == "tracert":
        tracert_command(protocol_info)
        filtered_packets = create_tracert_packets(captured_packets)
    elif protocol == "ftp":
        ftp_command()
        filtered_packets = create_ftp_packets(captured_packets)
    #if command not recognized
    else:
        return "error: command not recognized"
    return filtered_packets


