import socket
import time

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# Set a timeout so the socket does not block
# indefinitely when trying to receive data.

server.settimeout(0.2)

server.bind(("", 33333))
message = b"sync"
while True:
        server.sendto(message, ('192.168.5.255', 9013))
        #print("message sent!")
        time.sleep(4)

