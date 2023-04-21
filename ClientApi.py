import logging

from telethon import TelegramClient

from Chat import Chat
from ChatIter import ChatIter


class ClientApi:
    __log = logging.getLogger('__name__')

    def __init__(self, client: TelegramClient) -> None:
        self.__client = client
        self.__is_bot = None

    async def hasAccessToChatHistory(self, chat: Chat) -> bool:
        return not await self.is_bot()

    async def buildIter(self, chat: Chat, limit: int, start_message_id: int, downward: bool) -> ChatIter | None:
        if not await self.hasAccessToChatHistory(chat):
            self.__log.error(f"Client hasn't access to chat ({chat.id})_ history")
            return None
        else:
            return ChatIter(self.__client, chat.id, limit, start_message_id, downward)

    async def is_bot(self) -> bool:
        if self.__is_bot is None:
            self.__is_bot = await self.__client.is_bot()
        return self.__is_bot




# debuging

# async def debug():
#     from TelegramConfig import api_id, api_hash
#     client = await TelegramClient("not bot", api_id, api_hash).start()
#     api = ClientApi(client)
#     print(await api.is_bot())
#     from telethon.tl.types import PeerChannel
#     i = await api.buildIter(Chat(PeerChannel(1935611955)), 100, 0, False)
#     n = await i.next()
#     print(n.id.chat_id, n.id.message_id, n.message, n.reply_id)
#     n = await i.next()
#     print(n.id.chat_id, n.id.message_id, n.message, n.reply_id.chat_id, n.reply_id.message_id)
#     n = await i.next()
#     print(n.id.chat_id, n.id.message_id, n.message, n.reply_id)
#
# import asyncio
# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# asyncio.run(debug())
