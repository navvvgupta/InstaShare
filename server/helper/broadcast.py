def broadcast(message,clients):
    for client in clients:
        client.send(message)