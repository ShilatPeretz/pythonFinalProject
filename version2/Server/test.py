# this ia a test file to check the scapySniff file
from scapysniff import sniff_packets

filtered_packets = sniff_packets("tracert")
# for packet in filtered_packets:
#     packet.print_packet()