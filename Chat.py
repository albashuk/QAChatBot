from __future__ import annotations

from collections import deque

from telethon.tl.types import TypePeer, PeerUser, PeerChat, PeerChannel

from Dictionary import Dictionary


class Chat:
    class Id:
        def __init__(self, peed_id: 'TypePeer') -> None:
            self.peer_id = peed_id

        def __hash__(self):
            match self.peer_id:
                case PeerUser():
                    return hash((0, self.peer_id.user_id))
                case PeerChat():
                    return hash((1, self.peer_id.chat_id))
                case PeerChannel():
                    return hash((2, self.peer_id.channel_id))

        def __eq__(self, other: Chat.Id):
            return self.peer_id == other.peer_id

        def __str__(self):
            return str(self.peer_id)

        def value(self) -> int:
            match self.peer_id:
                case PeerUser():
                    return self.peer_id.user_id
                case PeerChat():
                    return self.peer_id.chat_id
                case PeerChannel():
                    return self.peer_id.channel_id

    def __init__(self, id: Id, dictionary: Dictionary = None) -> None:
        self.id = id
        self.dictionary = dictionary
        self.message_count = {"user": 0, "moderator": 0}
        self.questions_queue = {"user": deque(), "moderator": deque()}
        self.questions = {}  # TODO: use database
