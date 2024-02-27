import scapy.all

from scapysniff import sniff_packets

# scapy.all.show_interfaces()

filtered_packets = sniff_packets("ftp")