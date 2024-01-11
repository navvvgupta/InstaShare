import socket
import threading
import json
# Choosing Nickname
nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9999))

# global s
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host = '192.168.1.101'
# port = 9999
# s.connect((host, port))

# Listening to Server and Sending Nickname

def list_allUser(message):
    client.send(message.encode('utf-8'))
    list_user=client.recv(1024).decode("utf-8")
    user_map = json.loads(list_user)
    # print('HI')
    # print(user_map)
    # for username, ip_address in user_map.items():
    #     print(f"Username: {username}, IP Address: {ip_address}")

def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occurred!")
            client.close()
            break

# Sending Messages To Server
def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        if(message==f"{nickname}: list_all_user"):
            list_allUser(message)
        client.send(message.encode('utf-8'))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
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