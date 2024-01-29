import socket
import threading
from helper.receiveFile import receive_file

def client_conn(ip, file_name):
    client_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_conn.connect((ip, 10500))
    client_conn.send(file_name.encode('utf-8'))
    receive_file(client_conn)

def listen_messages(main_server_conn):
    while True:
        try:
            message = main_server_conn.recv(1024).decode('utf-8')
            # if message == 'NICK':
                # main_server_conn.send(nickname.encode('utf-8'))
            if message:
                print(message)
        except:
            # Close Connection When Error
            print("An error occurred!")
            main_server_conn.close()
            break

# Broadcasting messages through the main server
def send_message(main_server_conn, username):
    while True:
        user_input = input('')
        message = '{}: {}'.format(username, user_input)
        if "connect(" in user_input:
            start_index = user_input.find('(')
            end_index = user_input.find(')')
            ip = user_input[start_index + 1 : end_index]
            print(f'Enter the file/folder name you want from {ip}: ')
            file_name=input(r'')
            receive_thread = threading.Thread(target=client_conn, args=(ip, file_name))
            receive_thread.start()
        elif message:
            main_server_conn.send(message.encode('utf-8'))