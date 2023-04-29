from __future__ import annotations

import telethon
from telethon.tl.types import TypePeer

from Chat import Chat
from MessageInterpretation import MessageInterpretation


class Message:
    class Id:
        def __init__(self, chat_id: Chat.Id, message_id: int) -> None:
            self.chat_id = chat_id
            self.message_id = message_id

        def __hash__(self):
            return hash((self.chat_id, self.message_id))

        def __eq__(self, other: Message.Id):
            return self.chat_id == other.chat_id and self.message_id == other.message_id

    def __init__(self,
                 id: Id,
                 message: str,
                 from_id: 'TypePeer',
                 reply_id: Id = None,
                 is_from_moderator: bool = None,
                 is_question: bool = None,
                 interpretation: MessageInterpretation = None) -> None:
        self.id = id
        self.message = message
        self.from_id = from_id
        self.reply_id = reply_id
        self.is_from_moderator = is_from_moderator
        self.is_question = is_question
        self.interpretation = interpretation

    @classmethod
    def fromTelethonMessage(cls, tMessage: telethon.tl.custom.message.Message):
        reply_id = None \
            if tMessage.reply_to is None \
            else Message.Id(tMessage.peer_id, tMessage.reply_to.reply_to_msg_id)
        return Message(Message.Id(tMessage.peer_id, tMessage.id), tMessage.message, tMessage.from_id, reply_id)





# debugging

# id1 = Message.Id(PeerUser(123), 321)
# id2 = Message.Id(PeerChat(123), 321)
# id3 = Message.Id(PeerChannel(123), 321)
# print(hash(id1))
# print(hash(id2))
# print(hash(id3))


