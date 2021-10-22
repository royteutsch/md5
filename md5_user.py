from tkinter import *
import socket

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect(('127.0.0.1', 1729))


class Graphical_client:
    def __init__(self, lst, root):
        self.lst = lst
        self.total_rows = len(lst)
        self.frame = Frame(root)
        if not lst:
            self.total_columns = 0
        else:
            self.total_columns = len(lst[0])
        self.root = root

        # code for creating table
        for i in range(self.total_rows):
            for j in range(self.total_columns):
                self.e = Entry(self.frame, width=20, fg='black',
                               font=('Arial', 12, 'bold'))
                self.e.grid(row=i, column=j)
                self.e.insert(END, lst[i][j])
        self.root.after(100, self.update)

    def update(self):
        print("updating")
        my_socket.send("cd".encode())
        data = my_socket.recv(1024).decode()
        print(data)
        data = data[2:-2]
        data = data.split('], [')
        data = list(map(lambda x: x.split(", "), data))
        print(data)
        self.lst = data
        self.total_rows = len(self.lst)
        self.total_columns = len(self.lst[0])

        # code for creating table
        for i in range(self.total_rows):
            for j in range(self.total_columns):
                self.frame.pack_forget()
        # code for creating table
        for i in range(self.total_rows):
            for j in range(self.total_columns):
                self.e = Entry(self.root, width=20, fg='black',
                               font=('Arial', 12, 'bold'))
                self.e.grid(row=i, column=j, sticky=NSEW)
                self.e.insert(END, self.lst[i][j])
        self.root.after(1000, self.update)


rooty = Tk()
graphy = Graphical_client([], rooty)
rooty.mainloop()
