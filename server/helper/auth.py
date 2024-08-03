from ..models.user import User
import bcrypt
from .response_class import Response
from .listOnlineUser import listOnlineUser
import json


def isAuth(userInfo, client, clients, usernames):
    username = userInfo["username"]
    password = userInfo["password"]
    ip_address = userInfo["ip_address"]
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

        user = User.objects(username=username).first()
        if user and bcrypt.checkpw(
            password.encode("utf-8"), user.password.encode("utf-8")
        ):
            User.objects(username=username).update_one(
                set__ip_address=ip_address, set__is_online=True
            )
            clients.append(client)
            usernames.append(username)
            res = Response(
                is_message=True, is_auth=True, data="Authentication successful."
            )
            serialized_request = json.dumps(res.to_dict())
            client.send(serialized_request.encode())
            return True
        else:
            message = f"User not found or password incorrect."
            res = Response(is_message=True, data=message)
            serialized_request = json.dumps(res.to_dict())
            client.send(serialized_request.encode())
            print(f"User not found or password incorrect.")

    except Exception as e:
        message = f"Error during authentication: {str(e)}"
        res = Response(is_message=True, data=message)
        serialized_request = json.dumps(res.to_dict())
        client.send(serialized_request.encode())
        print(f"Error during authentication: {str(e)}")

    return False
