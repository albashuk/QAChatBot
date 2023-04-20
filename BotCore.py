import ClientApi
import Message


class BotCore:
    def __init__(self, clientApi: ClientApi) -> None:
        self.clientApi = clientApi
        self.__stats = {}         # TODO: use database
        self.__questions = {}     # TODO: use database
        self.__dictionaries = {}  # TODO: use database

    def messageProcessing(self, message: Message):
        pass

    def __isQuestion(self, message: Message):
        pass
