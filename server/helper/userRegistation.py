from ..models.user import User
import bcrypt
from .response_class import Response
from .listOnlineUser import listOnlineUser
import json


def userRegistration(userInfo, client, clients, usernames):

    try:
        # check for same ip address
        online_users_info = listOnlineUser()
        user_ip = userInfo.get("ip_address")
        ip_exists = any(user.get("ip_address") == user_ip for user in online_users_info)
        if ip_exists:
            res = Response(
                is_message=True,
                data="Currently ip_adress is used By other user.",
            )
            serialized_request = json.dumps(res.to_dict())
            client.send(serialized_request.encode())
            return False

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
            is_online=False,
        )
        new_user.save()
        clients.append(client)
        usernames.append(userInfo["username"])
        res = Response(
            is_message=True, data="Registration successful, Please Login 🙏."
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
