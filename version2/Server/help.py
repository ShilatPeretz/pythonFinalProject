#return the show as a string outpur
import io
import sys

file = "ftp/hello.txt"
file_path = "/version2/Server/ftp/hello.txt"


def get_packet_show_output(packet):
    # Redirect standard output to capture the string representation
    output_buffer = io.StringIO()
    sys.stdout = output_buffer

    # Call the show method to display packet details
    packet.show()

    # Restore standard output
    sys.stdout = sys.__stdout__

    # Get the captured string representation
    output_str = output_buffer.getvalue()

    return output_str