import multiprocessing
import threading
import socket
import hashlib

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect(('127.0.0.1', 1729))


x = True


def parse_data(inputted_data):
    if inputted_data[0] == "L":  # Server sent the start number and number of processes to be made for each core
        parameters = inputted_data[1:].split()
        start_number = parameters[0]
        processes = parameters[1]
        goal = parameters[2]
        for core in range(multiprocessing.cpu_count()):
            t = threading.Thread(target=decrypt(starting_num=(start_number + (core - 1) * processes),
                                                num_guesses=processes, goal=goal))
            t.start()


def decrypt(starting_num, num_guesses, goal):
    for i in range(int(num_guesses)):
        if hashlib.md5(str(int(starting_num) + i - 1).zfill(10).encode()).hexdigest() == goal:
            my_socket.send(
                (("S" + str(int(starting_num) + i - 1).zfill(10)).encode()))
            my_socket.close()
            exit()


while x:
    my_socket.send(("C" + str(multiprocessing.cpu_count())).encode())  # Sends the number of cpu cores
    data = my_socket.recv(1024).decode()
    parse_data(data)
