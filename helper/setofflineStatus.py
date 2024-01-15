from models.user import User

def setOfflineStatus(username):
    try:
        User.objects(username=username).update_one(set__is_online=False)
        print(f"User {username} is set to offline.")

    except Exception as e:
        print(f"Error while updating user status: {str(e)}")


