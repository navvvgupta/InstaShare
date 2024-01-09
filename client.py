import socket
import threading

global s
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.1.101'
port = 9999
s.connect((host, port))

def incoming_msg():
    global s
    while True:
        data = str(s.recv(1024).decode('utf-8'))
        if data:
            print(f"<server>  {data}")

def outgoing_msg():
    global s
    while True:
        msg = input()
        s.send(msg.encode("utf-8"))
        print('<client> ' + str(msg))

send_thread = threading.Thread(target=incoming_msg)
send_thread.start()

receive_thread = threading.Thread(target=outgoing_msg)
receive_thread.start()

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