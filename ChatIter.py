from telethon import TelegramClient, hints

from Message import Message


class ChatIter:
    def __init__(self,
                client: TelegramClient,
                entity: 'hints.EntityLike',
                limit: int,
                start_id: int,
                downward: bool) -> None:
        self.__iter = aiter(client.iter_messages(entity=entity,
                                                 limit=limit,
                                                 offset_id=start_id,
                                                 reverse=downward))

    async def next(self) -> Message:
        return Message.fromTelethonMessage(await anext(self.__iter))

