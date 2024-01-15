import socket
import threading
import select
import subprocess
import json

# Choosing Nickname
nickname = input("Choose your nickname: ")

metaData = {
    "username": "ajaySingh",
    "password": "123456789",
    "ip_address": "192.168.137.1",
    "isLoginAuth":"True"
}
metadata_json = json.dumps(metaData)

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.137.1', 9999))
client.send(metadata_json.encode('utf-8'))

# global s
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host = '192.168.1.101'
# port = 9999
# s.connect((host, port))

def clientfxn():
    print(1)
    global ip
    newclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    newclient.connect((ip, 10500))

# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            elif message:
                print(message)
        except:
            # Close Connection When Error
            print("An error occurred!")
            client.close()
            break

# Sending Messages To Server
def write():
    global ip
    while True:
        user_input = input('')
        message = '{}: {}'.format(nickname, user_input)
        if "connect(" in user_input:
            start_index = user_input.find('(')
            end_index = user_input.find(')')
            ip = user_input[start_index + 1 : end_index]
            clientfxn()
        elif message:
            client.send(message.encode('utf-8'))

#create socket
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 10500
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket created")

    except socket.error as msg:
        print("Socket creation error: " + str(msg))

# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()

# Establish connection with a client (socket must be listening)
def socket_accept():
    global conn
    global s
    sockets_list = [s]
    while True:
        read_sockets, _, _ = select.select(sockets_list, [], [])

        # for notified_socket in read_sockets:
        #     if notified_socket == s:
        #         accept_connection = input(f"Do you want to accept the connection from {notified_socket}? (yes/no): ")
        #         if accept_connection.lower() == "yes":
                    # subprocess.run(['start', 'cmd'], shell=True)
        conn, address = s.accept()
        print("Connection has been established! |" + " IP " + address[0] + " | Port" + str(address[1]))
        conn.send("Connected to the server!".encode('utf-8'))
        subprocess.run(['start', 'cmd'], shell=True)
                    # subprocess.run(['start', 'cmd', '/k', 'python', 'your_server_script.py'])
        return conn

                # else:
                #     print("Connection not accepted.")
                #     return

def server():
    create_socket()
    bind_socket()
    socket_accept()


    # subprocess.run(['start', 'cmd', '/k', 'python', 'your_server_script.py'])

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

server_thread = threading.Thread(target=server)
server_thread.start()

client_thread = threading.Thread(target=clientfxn)
# file = open("test_file/test.txt", "r")
# data = file.read()

# s.send("test.txt".encode("utf-8"))
# msg = s.recv(1024).decode("utf-8")
# print(f"[SERVER]: {msg}")

# s.send(data.encode("utf-8"))
# msg = s.recv(1024).decode("utf-8")
# print(f"[SERVER]: {msg}")
# file.close()
# s.close()