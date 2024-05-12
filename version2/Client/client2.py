import socket
import time

from version2.Client.client import connect_to_server, client_socket_send_protocol

if connect_to_server('login', "username", "password"):
    client_socket_send_protocol("http", "http")
    print("First try completed")
    time.sleep(5)  # Introduce a delay of 5 seconds
    print("Second try")
    client_socket_send_protocol("http", "HTTP")
