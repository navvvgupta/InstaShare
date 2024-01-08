import socket
import sys
import select

SIZE = 1024
FORMAT = "utf-8"
# Create a Socket ( connect two computers)
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()

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
    global s
    sockets_list = [s]
    while True:
        read_sockets, _, _ = select.select(sockets_list, [], [])

        for notified_socket in read_sockets:
            if notified_socket == s:
                accept_connection = input("Do you want to accept the connection? (yes/no): ")
                if accept_connection.lower() == "yes":
                    conn, address = s.accept()
                    print("Connection has been established! |" + " IP " + address[0] + " | Port" + str(address[1]))
                    send_commands(conn)
                    conn.close()
                    return  

                else:
                    print("Connection not accepted.")
                    return

# Send commands to client/victim or a friend
def send_commands(conn):
    while True:        
        #file ka name recieve kiya
        filename = conn.recv(1024).decode(FORMAT)
        if(filename == ""):
            conn.close()
            s.close()
            sys.exit()
        print(filename)
        print(f"[RECV] Receiving the filename.")
        file = open(filename, "w")
        conn.send("Filename received.".encode(FORMAT))

        #file ka data recieve kiya
        data = conn.recv(SIZE).decode(FORMAT)
        print(f"[RECV] Receiving the file data.")
        file.write(data)
        conn.send("File data received".encode(FORMAT))

        file.close()

def main():
    create_socket()
    bind_socket()
    socket_accept()


main()