#Creator: Faa Diallo
#Date: 02/25/2024
#This program creates a multi-threaded chat server. The corresponding
#client.py file is able to send messages to this server.
import socket
from _thread import *
import threading

client_names = {}

def main():
    """ Parameters: None
        Return: None
        This function creates a loopback UDP socket and runs threads
        for each of the client sockets that send messages to it.
    """
    local_ip = "127.0.0.1"
    local_port = 20001 
    buffer_size = 1024
    print_lock = threading.Lock()

    #Creates an IPv4 UDP socket
    udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    #Bind socket to IP and port
    udp_server_socket.bind((local_ip, local_port))
    print("UDP server up and listening")

    #Creates a thread for each connection to the server.
    threading.Thread(target=client_socket_thread, 
        args=(print_lock, udp_server_socket, buffer_size)).start()

def client_socket_thread(print_lock, udp_server_socket, buffer_size):
    """ Parameters: print_lock: Lock to prevent collisions in printing to stdout
                    udp_server_socket: UDP socket for the server
                    buffer_size: Maximum size block of text clients are able to send to server
        Return: None
        This function loops takes in input from any client and sends that input
        to all of the clients sending messages to and from the server.
    """
    exit = False
    while not exit:
        message, address = udp_server_socket.recvfrom(buffer_size)
        message = message.decode('UTF-8').rstrip()

        in_dictionary = client_names.get(address)
        client_names[address] = client_names.get(address, message) 

        if in_dictionary:
            output = f"> {client_names[address]}: {message}"
        else:
            output = f"> {client_names[address]} has entered the server."

        if message.rstrip() == "exit":
            exit = True
            output = f"> {client_names[address]} has exited the server."

        print_lock.acquire()
        print(output)
        print_lock.release()

        for ip_address in client_names:
            udp_server_socket.sendto(bytes(output, 'UTF-8'), ip_address)
            
    client_names.pop(address) 

if __name__ == "__main__":
    main() 
