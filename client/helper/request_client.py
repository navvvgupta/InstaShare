class ClientRequest:

    def __init__(self, filename, packet_offset):
        self.filename = filename
        self.packet_offset = packet_offset

    def to_dict(self):
        return {"filename": self.filename, "packet_offset": self.packet_offset}
