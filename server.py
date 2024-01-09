import socket
import sys
import select
import threading
FORMAT = "utf-8"

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

#create socket
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

# Establish connection with a client (socket must be listening)
def socket_accept():
    global conn
    global s
    sockets_list = [s]
    while True:
        read_sockets, _, _ = select.select(sockets_list, [], [])

        for notified_socket in read_sockets:
            if notified_socket == s:
                accept_connection = input(f"Do you want to accept the connection from {notified_socket}? (yes/no): ")
                if accept_connection.lower() == "yes":
                    conn, address = s.accept()
                    print("Connection has been established! |" + " IP " + address[0] + " | Port" + str(address[1]))
                    conn.send("Connected to the server!".encode('utf-8'))
                    return conn

                else:
                    print("Connection not accepted.")
                    return

# Send commands to client/victim or a friend
def send_file():
    while True:        
        #file ka name received
        filename = conn.recv(1024).decode(FORMAT)
        if(filename == ""):
            conn.close()
            s.close()
            sys.exit()
        print(filename)
        print(f"[RECV] Receiving the filename.")
        file = open(filename, "w")
        conn.send("Filename received.".encode(FORMAT))

        #file ka data received
        data = conn.recv(1024).decode(FORMAT)
        print(f"[RECV] Receiving the file data.")
        file.write(data)
        conn.send("File data received".encode(FORMAT))

        file.close()

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = s.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def main(): 
    create_socket()
    bind_socket()
    receive()

main()