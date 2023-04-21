import logging

from Chat import Chat
from ClientApi import ClientApi
from Message import Message


class BotCore:
    __log = logging.getLogger('__name__')

    def __init__(self, clientApi: ClientApi) -> None:
        self.__clientApi = clientApi
        self.__stats = {}         # TODO: use database
        self.__chats = {}         # TODO: use database
        self.__dictionaries = {}  # TODO: use database

    def messageProcessing(self, message: Message):
        pass

    def initChatQuestions(self, chat: Chat):
        if not self.__clientApi.hasAccessToChatHistory(chat):
            self.__log.warning(f"Client hasn't access to chat ({chat.id})_ history")
            return

        pass

    def __isQuestion(self, message: Message):
        pass

    def __ChatFromMessage(self, message: Message):
        return self.__chats[message.id.chat_id]