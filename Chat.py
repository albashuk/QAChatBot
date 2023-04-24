from collections import deque

from telethon.tl.types import TypePeer


class Chat:
    def __init__(self, id: 'TypePeer') -> None:
        self.id = id
        self.message_count = {"user": 0, "moderator": 0}
        self.questions_queue = {"user": deque(), "moderator": deque()}
        self.questions = {}  # TODO: use database
