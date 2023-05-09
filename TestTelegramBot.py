from telethon.tl.types import PeerChannel

import main
from BotCore import BotCore
from Chat import Chat
from ClientApi import ClientApi
from Dictionary import Dictionary


class TestBotCore(BotCore):
    def setChatDictionary(self, chat_id: Chat.Id, dictionary: Dictionary):
        chat = self._BotCore__chatById(chat_id)
        chat.dictionary = dictionary


main.botCore = TestBotCore(ClientApi(main.client))
words = {"Ukraine", "Kyiv", "medicament", "Insulin"}
dictionary = Dictionary(words)
main.botCore.setChatDictionary(Chat.Id(PeerChannel(1935611955)), dictionary)


main.main()

