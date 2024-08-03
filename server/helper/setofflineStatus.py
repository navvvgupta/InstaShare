from models.user import User
from termcolor import colored


def setOfflineStatus(username):
    try:
        User.objects(username=username).update_one(set__is_online=False)
        message = f"User {username} is set to offline."
        colored_message = colored(message, "yellow")
        print(colored_message)

    except Exception as e:
        print(f"Error while updating user status: {str(e)}")
