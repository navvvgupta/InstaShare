import socket
import threading
import json
import select
global main_server_conn
BUFFER_SIZE = 1024
SEPARATOR = '<SEPARATOR>'
metaData = {
    "username": "ajaySingh",
    "password": "123456789",
    "ip_address": "192.168.137.1",
    "isLoginAuth":"True"
}
serverIP = '192.168.137.1'
metadata_json = json.dumps(metaData)

from helper.sendFile import send_file
import helper.chatRoom as chat


def connect_to_main_server():
    global main_server_conn
    try:
        main_server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        main_server_conn.connect((serverIP, 9999))
        main_server_conn.send(metadata_json.encode('utf-8'))
        print("Connected to the main server!")
    except socket.error as msg:
        print("Socket creation error: " + str(msg))

# File transfer server(runs on every client)
def file_transfer_server():
    file_transfer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockets_list = [file_transfer_socket]
    try:
        print("File transfer server is running...")
        host = ""
        port = 10500
        file_transfer_socket.bind((host, port))
        file_transfer_socket.listen()
        while True:
            read_sockets, _, _ = select.select(sockets_list, [], [])
            for notified_socket in read_sockets:
                if notified_socket == file_transfer_socket:
                    file_transfer_conn, address = file_transfer_socket.accept()
                    send_file_thread = threading.Thread(target=send_file, args=(file_transfer_conn,))
                    send_file_thread.start()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))

username = metaData["username"]

def main():
    main_server_conn = connect_to_main_server()
    if main_server_conn:
        username = metaData["username"]

        broadcast_message_thread = threading.Thread(target=chat.send_message, args=(main_server_conn, username))
        broadcast_message_thread.start()

        listen_message_thread = threading.Thread(target=chat.listen_messages, args=(main_server_conn,))
        listen_message_thread.start()

        file_transfer_server_thread = threading.Thread(target=file_transfer_server)
        file_transfer_server_thread.start()

        broadcast_message_thread.join()
        listen_message_thread.join()
        file_transfer_server_thread.join()

if __name__ == "__main__":
    main()