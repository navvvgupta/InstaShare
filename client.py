import socket
import threading
import tqdm
import os

BUFFER_SIZE = 1024
SEPARATOR = '<SEPARATOR>'
nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.137.1', 9999))

def receive_file(newclient):
    received = newclient.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    # remove absolute path if there is
    filename = os.path.basename(filename)
    # convert to integer
    filesize = int(filesize)
    # start receiving the file from the socket
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        while True:
            # read 1024 bytes from the socket (receive)
            bytes_read = newclient.recv(BUFFER_SIZE)
            if not bytes_read:    
                progress.close()
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            progress.update(len(bytes_read))

def send_file():
    filename = "About.Time.2013.720p.x264.English.Hindi.mkv"
    filesize = os.path.getsize(filename)
    conn.send(f"{filename}{SEPARATOR}{filesize}".encode())
    # start sending the file
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                progress.close()
                break
            # we use sendall to assure transmission in busy networks
            conn.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))

def clientfxn():
    print(1)
    global ip
    newclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    newclient.connect((ip, 10500))
    msg = newclient.recv(1024).decode('utf-8')
    print(msg)
    receive_file(newclient)

# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
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
    while True:
        print("after while")
        print("in accept fxn")

        conn, address = s.accept()
        print("Connection has been established! |" + " IP " + address[0] + " | Port" + str(address[1]))
        conn.send("Connected to the client server!".encode('utf-8'))
        return conn

def server():
    create_socket()
    bind_socket()
    socket_accept()
    send_file()


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

server_thread = threading.Thread(target=server)
server_thread.start()