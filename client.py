#Creator: Faa Diallo
#Date: 02/25/2024
#This program is a client for a multi-threaded chat server. 
import socket
import select
import sys

udp_server_socket = None

def main():
	""" Parameters: None 
		Return: None
		This function creates a socket to connect to the UDP loopback
		server. It then either takes in input from the user to send
		to the server or prints out messages sent from the server to
		the client.
	"""
	global udp_server_socket
	exit = False
	buffer_size = 1024
	server_address_port = ("127.0.0.1", 20001)
	udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

	while not exit:
		sys.stdout.write("> ")
		sys.stdout.flush()

		read_list = [sys.stdin, udp_server_socket] 

		# Looks at the lists of file descriptors and returns when
		# at least one of them is ready to be read.
		ready_to_read, _, _ = select.select(read_list, [], [])


		for fd in ready_to_read:
			if fd == udp_server_socket:
				# Reads in a message from the server and prints it.
				message, address = udp_server_socket.recvfrom(buffer_size)
				msg = f"{message.decode('UTF-8')}"
				print(msg)
			else:
				# Reads in a message from the client and sends it to the server.
				msg_from_client = sys.stdin.readline()
				if msg_from_client.rstrip() == "exit": exit = True
				udp_server_socket.sendto(bytes(msg_from_client, "UTF-8"), server_address_port)
	
def exit_program():
	print("Exiting the UDP client.")
	udp_server_socket.close()
	sys.exit(0)

if __name__ == '__main__':
	try:
		main()
		exit_program()
	except KeyboardInterrupt:
		exit_program()
