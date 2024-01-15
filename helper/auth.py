from models.user import User
import bcrypt

def isAuth(userInfo,client,clients,usernames):
    username=userInfo['username']
    password=userInfo['password']
    try:
        user = User.objects(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            User.objects(username=username).update_one(set__is_online=True)
            clients.append(client)
            usernames.append(username)
            client.send('Authentication successful.'.encode('utf-8'))
            return

    except Exception as e:
        print(f"Error during authentication: {str(e)}")

    return 
