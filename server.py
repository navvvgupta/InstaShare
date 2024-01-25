import socket
import sys
import os
import tqdm
SIZE = 1024
FORMAT = "utf-8"
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024  # send 4096 bytes each time step
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
    conn, address = s.accept()
    print("Connection has been established! |" + " IP " + address[0] + " | Port" + str(address[1]))
    send_commands(conn)
    conn.close()

def receive_file(client_conn):
    try:
        file_info_data = client_conn.recv(BUFFER_SIZE).decode('utf-8')
        file_name_here, file_size = file_info_data.split(SEPARATOR)
        print('Hello')
        receive_single_file(client_conn, file_info_data)

    except Exception as e:
        print(f"Error during file/folder reception: {e}")
    finally:
        # Close the connection after completing the file/folder reception
        client_conn.close()

def receive_single_file(client_conn, file_info_data):
    try:
        filename, filesize = file_info_data.split(SEPARATOR)
        filename = os.path.basename(filename)
        filesize = int(filesize)

        progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "wb") as f:
            while True:
                bytes_read = client_conn.recv(BUFFER_SIZE)
                if not bytes_read:
                    progress.close()
                    f.close()
                    break
                f.write(bytes_read)
                progress.update(len(bytes_read))

    except Exception as e:
        print(f"Error during file reception: {e}")
# Send commands to client/victim or a friend
def send_commands(conn):      
        receive_file(conn)
def main():
    create_socket()
    bind_socket()
    socket_accept()


main()