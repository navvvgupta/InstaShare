import json
from helper.response_class import Response


def broadcast(message, clients):
    for client in clients:
        try:
            # print(message)
            res = Response(is_message=True, data=message)
            serialized_request = json.dumps(res.to_dict())
            client.send(serialized_request.encode())
        except Exception as e:
            print(e)
            break
