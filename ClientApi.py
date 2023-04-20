from telethon import TelegramClient


class ClientApi:
    def __int__(self, client: TelegramClient):
        self.__client = client
        self.__is_bot = client.is_bot()
