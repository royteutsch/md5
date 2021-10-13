import socket

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect(('127.0.0.1', 1729))

x = True

while x:
    user_request = input("Would you like to see the [c]urrent number, see the [n]umber of clients, or the [h]ash?")
    if user_request != "c" and user_request != "n" and user_request != "h":
        print("Invalid Request!")
    else:
        my_socket.send(user_request.encode())
        data = my_socket.recv(1024).decode()
        print(data)
