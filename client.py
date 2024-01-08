import socket
import os
import subprocess

s = socket.socket()
host = '192.168.137.78'
port = 9999

s.connect((host, port))

file = open("abhinav/test.txt", "r")
data = file.read()

s.send("test.txt".encode("utf-8"))
msg = s.recv(1024).decode("utf-8")
print(f"[SERVER]: {msg}")

s.send(data.encode("utf-8"))
msg = s.recv(1024).decode("utf-8")
print(f"[SERVER]: {msg}")
file.close()
s.close()