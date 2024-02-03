from models.user import User
import bcrypt

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
            client.send('Authentication successful.'.encode('utf-8'))
            print(":)")
            return True

    except Exception as e:
        client.send(f"Error during authentication: {str(e)}".encode('utf-8'))
        print(f"Error during authentication: {str(e)}")

    return False
