from models.user import User
import bcrypt
from helper.response_class import Response
import json

def isAuth(userInfo,client,clients,usernames):
    username=userInfo['username']
    password=userInfo['password']
    ip_address=userInfo['ip_address']
    try:
        user = User.objects(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            User.objects(username=username).update_one(set__ip_address=ip_address,set__is_online=True)
            clients.append(client)
            usernames.append(username)
            res = Response(is_message=True,data='Authentication successful.')
            serialized_request = json.dumps(res.to_dict())
            client.send(serialized_request.encode())
            print(":)")
            return True

    except Exception as e:
        message=f"Error during authentication: {str(e)}"
        res = Response(is_message=True,data=message)
        serialized_request = json.dumps(res.to_dict())
        client.send(serialized_request.encode())
        print(f"Error during authentication: {str(e)}")

    return False
