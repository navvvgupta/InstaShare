import json
from helper.response_class import Response


def broadcast(message, clients):
    for client in clients:
        try:
            print("object 1")
            print(clients)
            res = Response(is_message=True, data=message)
            print(res)
            print("object 2")
            serialized_request = json.dumps(res.to_dict())
            print(serialized_request)
            print("object 3")
            client.send(serialized_request.encode())
            print("hogaya")
        except Exception as e:
            print("Error idhar aayi hai")
            print(e)
            break
