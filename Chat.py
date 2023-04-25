from collections import deque

from telethon.tl.types import TypePeer

from Dictionary import Dictionary


class Chat:
    def __init__(self, id: 'TypePeer', dictionary: Dictionary = None) -> None:
        self.id = id
        self.dictionary = dictionary
        self.message_count = {"user": 0, "moderator": 0}
        self.questions_queue = {"user": deque(), "moderator": deque()}
        self.questions = {}  # TODO: use database
