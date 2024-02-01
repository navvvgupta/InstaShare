import json
from models.user import User

def listOnlineUser():
    try:
        online_users = User.objects(is_online=True)
        online_user_info = [{'username': user.username, 'ip_address': user.ip_address} for user in online_users]
        online_user_info_json = json.dumps(online_user_info)
        return online_user_info_json

    except Exception as e:
        print(f"Error while listing online users: {str(e)}")
        return []
