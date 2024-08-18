class Response:

    def __init__(
        self,
        is_message=False,
        list_public_file_data=False,
        search_by_file_result=False,
        list_online_user=False,
        is_auth=False,
        search_file_user_result=False,
        uploadFile=False,
        data=None,
    ):
        self.header = {
            "isMessage": is_message,
            "listPublicFile": list_public_file_data,
            "listOnlineUser": list_online_user,
            "searchByFile": search_by_file_result,
            "isAuth": is_auth,
            "search_file_user": search_file_user_result,
            "uploadFile": uploadFile,
        }

        self.body = {"data": data}

    def to_dict(self):
        return {"header": self.header, "body": self.body}
