import telethon

from telethon.tl.types import TypePeer


class Message:
    class Id:
        def __init__(self, chat_id: 'TypePeer', message_id) -> None:
            self.chat_id = chat_id
            self.message_id = message_id

    def __init__(self,
                 id: Id,
                 message: str,
                 reply_id: Id = None,
                 is_from_moderator: bool = None) -> None:
        self.id = id
        self.message = message
        self.reply_id = reply_id
        self.__is_from_moderator = is_from_moderator

    @classmethod
    def fromTelethonMessage(cls, tMessage: telethon.tl.custom.message.Message):
        reply_id = None \
            if tMessage.reply_to is None \
            else Message.Id(tMessage.peer_id, tMessage.reply_to.reply_to_msg_id)
        return Message(Message.Id(tMessage.peer_id, tMessage.id), tMessage.message, reply_id)

    def isFromModerator(self) -> bool:
        if self.__is_from_moderator is not None:
            return self.__is_from_moderator
        else:
            pass



