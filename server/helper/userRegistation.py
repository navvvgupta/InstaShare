from models.user import User
import bcrypt
from helper.response_class import Response
import json


def userRegistration(userInfo, client, clients, usernames):
    print("inside userRegistration")
    try:
        existing_user = User.objects(username=userInfo["username"]).first()
        if existing_user:
            res = Response(
                is_message=True,
                data="Username already exists. Choose a different username.",
            )
            serialized_request = json.dumps(res.to_dict())
            client.send(serialized_request.encode())
            return False

        hashed_password = bcrypt.hashpw(
            userInfo["password"].encode("utf-8"), bcrypt.gensalt()
        )

        new_user = User(
            username=userInfo["username"],
            password=hashed_password.decode("utf-8"),
            ip_address=userInfo["ip_address"],
            is_online=True,
        )
        new_user.save()
        clients.append(client)
        usernames.append(userInfo["username"])
        res = Response(
            is_message=True, data="Registration successful. Connected to server."
        )
        serialized_request = json.dumps(res.to_dict())
        client.send(serialized_request.encode())
        return True

    except Exception as e:
        message = f"Registration failed. Error: {str(e)}"
        res = Response(is_message=True, data=message)
        serialized_request = json.dumps(res.to_dict())
        client.send(serialized_request.encode())
        return False
