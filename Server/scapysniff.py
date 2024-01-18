## this file will collect all packets and extract the wanted data
## **connect to server
import subprocess
import scapy.all as scapy

def http_command():
    http_command = f"curl http://www.facebook.com"
    subprocess.run(http_command, shell=True)

# Scapy sniffs from all the netwrk interface/
# But we can ask Scapy to sniff only on a specific interface
def sniff_packets(command):
    process_packets = []
    num_packets_to_capture = 100
    global captured_packets
    if command == "http":
        captured_packets = scapy.sniff(prn=http_command(),count=650)
        process_packets_http()
    elif command == "else":
        captured_packets = scapy.sniff(count=num_packets_to_capture)
    print(len(captured_packets))
    print(captured_packets.summary())

def process_packets_http():
    return 0


