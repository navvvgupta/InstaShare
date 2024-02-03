import socket
import threading
from helper.receiveFile import receive_file
from helper.request_class import Request
import pickle

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
        
        # connect to other client for data sharing
        if "connect(" in user_input:
            start_index = user_input.find('(')
            end_index = user_input.find(')')
            ip = user_input[start_index + 1 : end_index]
            print(f'Enter the file/folder name you want from {ip}: ')
            file_name=input(r'')
            receive_thread = threading.Thread(target=client_conn, args=(ip, file_name))
            receive_thread.start()
        
        #  request to common server
        elif message:
            print("1")
            if "list_all_user" in user_input:
                print("2")
                req = Request(is_online_user=True)
                serialized_request = pickle.dumps(req)
                main_server_conn.send(serialized_request)
            
            elif "close" in user_input:
                print("3")
                req=Request(is_system=True)
                serialized_request = pickle.dumps(req)
                main_server_conn.send(serialized_request)
            
            else:
                print("4")
                req=Request(is_message=True, content=message)
                print(req.body['content'])
                serialized_request = pickle.dumps(req)
                print(serialized_request)
                main_server_conn.send(serialized_request)