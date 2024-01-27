## this file will collect all packets and extract the wanted data
## **connect to server
import subprocess
from scapy.sendrecv import AsyncSniffer
from packet_filter import http_packet_filter
from help import site

#the captured packets will be saved here
captured_packets = []

# Append the packet to the list
def capture_packets(packet):
    captured_packets.append(packet)

def http_command():
    sniff_thread = AsyncSniffer(prn=capture_packets, count=25)
    sniff_thread.start()

    # Execute your command (replace with your actual command)
    command_to_execute = f"curl http://{site}"
    subprocess.Popen(command_to_execute, shell=True).wait()


# Scapy sniffs from all the netwrk interface/
# But we can ask Scapy to sniff only on a specific interface
def sniff_packets(command):
    if command == "http":
        http_command()
        filtered_packets = http_packet_filter(captured_packets)
    elif command == "else":
        #other command function
        return
    #if command not recognized
    else:
        return "error: command not recognized"
    print(len(captured_packets))
    return filtered_packets


