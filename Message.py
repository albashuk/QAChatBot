from telethon.tl.types import TypePeer


class Message:
    class MessageId:
        def __int__(self, peer_id: 'TypePeer', message_id) -> None:
            self.peer_id = peer_id
            self.message_id = message_id

    def __init__(self,
                 id: MessageId,
                 text: str,
                 replyMessageId: MessageId = None,
                 is_from_moderator: bool = None) -> None:
        self.id = id
        self.text = text
        self.replyMessageId = replyMessageId
        self.__is_from_moderator = is_from_moderator

    def isFromModerator(self) -> bool:
        if self.__is_from_moderator is not None:
            return self.__is_from_moderator
        else:
            pass



