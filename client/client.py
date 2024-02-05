import socket
import threading
import json
import select
import inquirer
from helper.get_lan_ip import get_lan_ip
global main_server_conn
BUFFER_SIZE = 1024
SEPARATOR = '<SEPARATOR>'

# client ip address 
CLIENT_IP = get_lan_ip()
print(CLIENT_IP)
metaData = {
    "username": "ajay",
    "password": "123456789",
    "ip_address": CLIENT_IP,
}
serverIP = '192.168.68.140'
global metadata_json
metadata_json = json.dumps(metaData)

from helper.sendFile import send_file
import helper.chatRoom as chat


def connect_to_main_server(metadata_json):
    global main_server_conn
    try:
        main_server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        main_server_conn.connect((serverIP, 9999))
        main_server_conn.send(metadata_json.encode('utf-8'))
        auth = main_server_conn.recv(BUFFER_SIZE).decode('utf-8')
        if "successful" in auth:
            return True
        elif auth:
            main_server_conn.close()
            return False
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
    global metadata_json
    global main_server_conn
    questions = [
        inquirer.List('action',
                  message="Select an option:",
                  choices=['Register', 'Login'],
                  ),
    ]

    answers = inquirer.prompt(questions)
    selected = answers['action']
    # username = input('Enter your username: ')
    # password = input('Enter your password: ')
    # ip = input('Enter your IP: ')
    metadata_dict = json.loads(metadata_json)
    if selected == 'Register':
        metadata_dict["isLoginAuth"] = "False"
    if selected == 'Login':
        metadata_dict["isLoginAuth"] = "True"
    msg = json.dumps(metadata_dict)
    print(msg)
    flag = connect_to_main_server(msg)
    if flag:

        broadcast_message_thread = threading.Thread(target=chat.send_message, args=(main_server_conn, username))
        broadcast_message_thread.start()

        listen_message_thread = threading.Thread(target=chat.listen_messages, args=(main_server_conn,))
        listen_message_thread.start()

        file_transfer_server_thread = threading.Thread(target=file_transfer_server)
        file_transfer_server_thread.start()

        broadcast_message_thread.join()
        listen_message_thread.join()
        file_transfer_server_thread.join()

# if __name__ == "__main__":
main()