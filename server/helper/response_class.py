
class Response:
    def __init__(self, is_message=False, is_system=False, is_file_sharing=False, is_public_file=False,
                 is_online_user=False, data=None):
        self.header = {
            'isMessage': is_message,
            'isSystem': is_system,
            'isFileSharing': is_file_sharing,
            'isPublicFile': is_public_file,
            'isOnlineUser': is_online_user
        }

        self.body = {
            'data': data
        }
    
    def to_dict(self):
        return {'header': self.header, 'body': self.body}
