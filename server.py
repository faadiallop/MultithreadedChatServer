#Creator: Faa Diallo
#Date: 02/25/2024
#This program creates a multi-threaded chat server. The corresponding
#client.py file is able to send messages to this server.
import socket
from _thread import *
import threading

def main():

    local_ip = "127.0.0.1"
    local_port = 20001 
    buffer_size = 1024
    msg_from_server = "Message received on UDP Client and sending it again: "

    #Creates an IPv4 UDP socket
    udp_server_socket = socket.socket(family=socket.AF_INET, type=SOCK_DGRAM)

    #Bind socket to IP and port
    udp_server_socket.bind((local_ip, local_port))

    print("UDP server up and listening")

    while(True):
        message, address = udp_server_socket.recvfrom(buffer_size)

        print(f"\nMessage from Client:{message.decode('UTF-8')}")
        print(f"Client IP Address {address}")

        bytes_to_send = msg_from_server + message.decode('UTF-8')

        udp_server_socket.sendto(str.encode(bytes_to_send), address)

if __name__ == "__main__":
    main() 
