import json
from ..models.user import User


def listOnlineUser():
    try:
        online_users = User.objects(is_online=True)
        online_user_info = [
            {"username": user.username, "ip_address": user.ip_address}
            for user in online_users
        ]
        return online_user_info

    except Exception as e:
        print(f"Error while listing online users: {str(e)}")
        return []
