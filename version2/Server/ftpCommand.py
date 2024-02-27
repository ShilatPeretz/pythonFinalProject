import threading
import time
from version2.Server.ftp.ftpServerScript import server_main
from version2.Server.ftp.ftpClientScript import client_main


def execute_ftp_command():
    # Flag to indicate if the server should continue running
    server_running = threading.Event()
    server_running.set()  # Set the flag to True initially

    # Create a thread to run the server
    server_thread = threading.Thread(target=server_main, args=(server_running,))
    server_thread.start()

    # Allowing some time for the server to start up (optional)
    time.sleep(1)

    # Execute the client
    client_main()

    # After client_main finishes, clear the flag to stop the server
    server_running.clear()

    # Wait for the server thread to finish
    server_thread.join()



