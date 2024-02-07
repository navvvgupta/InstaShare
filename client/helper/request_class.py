class Request:
    def __init__(self,upload_to_public_folder=False, is_message=False, close_system=False,search_by_file=False,list_public_data=False,list_online_user=False,data=None):
        self.header = {
            'searchByFile': search_by_file,
            'UploadToPublicFolder': upload_to_public_folder,
            'isMessage': is_message,
            'closeSystem': close_system,
            'listPublicData': list_public_data,
            'listOnlineUser': list_online_user,
        }

        self.body = {
            'data': data
        }
    
    def to_dict(self):
        return {'header': self.header, 'body': self.body}
