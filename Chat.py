from telethon.tl.types import TypePeer


class Chat:
    def __init__(self, id: 'TypePeer') -> None:
        self.id = id
        self.questions = {}  # TODO: use database
