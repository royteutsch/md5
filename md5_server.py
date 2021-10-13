import select
import socket

""" Socket Parameters """
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 1729))
server_socket.listen()
client_sockets = []

""" Decrypting Parameters """
NUM_OF_TRIES = 1000  # Number of tries per cores
START_NUMBER = 5000000000  # Number which we start from
GOAL = "EC9C0F7EDCC18A98B1F31853B1813301"  # The goal of the hash
FAILURE = True

while FAILURE:
    rlist, wlist, xlist = select.select([server_socket] + client_sockets, [], [])
    if FAILURE:
        for current_socket in rlist:
            if current_socket is server_socket:
                connection, client_address = current_socket.accept()
                print("New client joined!", client_address)
                client_sockets.append(connection)
            else:
                data = current_socket.recv(1024).decode()
                # print("data: " + data)
                if data == "" or data == "EXIT":
                    print("Connection closed: " + str(client_address))
                    client_sockets.remove(current_socket)
                    rlist.remove(current_socket)
                    current_socket.close()
                else:
                    if data[0] == "C":  # Client sent us the number of cores he has
                        # print("Number of Cores for: " + str(client_address) + " is: " + data[1:])
                        processes = int(data[1:]) * NUM_OF_TRIES
                        response = "L"+str(START_NUMBER) + " " + str(processes) + " " + GOAL
                        current_socket.send(response.encode())
                        START_NUMBER += int(processes)
                    elif data[0] == "S":  # Client was successful, stop all the processes
                        print("Decryption successful, number is: " + data[1:])
                        FAILURE = False
                    elif data[0] == "c":  # User client asked for the current number
                        current_socket.send(("Current Number is: " + str(START_NUMBER)).encode())
                    elif data[0] == "n":  # User Client asked for the number of clients
                        current_socket.send(("Current Number of clients is: " + str(len(client_sockets))).encode())
                    elif data[0] == "h":  # User Client asked for the hash we're trying to crack
                        current_socket.send(("The Hash we're trying to decrypt is: " + GOAL).encode())
        print("Current Number: " + str(START_NUMBER).zfill(10))
    if not FAILURE:
        for current_socket in rlist:
            print("Connection closed: " + str(client_address))
            client_sockets.remove(current_socket)
            rlist.remove(current_socket)
            current_socket.close()
