import asyncio

from telethon.tl.types import PeerChannel, PeerUser

from BotCore import BotCore
from Chat import Chat
from ClientApi import ClientApi
from Dictionary import Dictionary
from Message import Message


class TestBotCore(BotCore):
    def setChatDictionary(self, chat_id: Chat.Id, dictionary: Dictionary):
        chat = self._BotCore__chatById(chat_id)
        chat.dictionary = dictionary

    async def messageProcessing(self, message: Message, with_answering: bool = True):
        # return str(message.id) + " " + str(message.from_id) + " " + str(message.reply_id) + " " + str(message.is_from_moderator) + "\n" + message.message
        return await super().messageProcessing(message)


async def main():
    messages = [
        (1, True, "Hey! Does anyone know where I can find Insulin in Kyiv?"),
        (2, True, "No, sorry, I don't know where to find insulin."),
        (3, True, "Yeh, me too."),
        (4, True, "You can find it at the pharmacy on Zelena Street. This is the only place in Kyiv that is selling insulin."),
        (1, True, "Thanks!"),
        (5, True, "Hello! Don't know where to find Insulin. Could anyone help me, please? That's critical!"),
    ]

    words = {"Ukraine", "Kyiv", "medicament", "Insulin"}
    dictionary = Dictionary(words)

    chat_id = Chat.Id(PeerChannel(123))
    full_messages = [Message(Message.Id(chat_id, i), message[2], PeerUser(message[0]), None, message[1]) for i, message in enumerate(messages)]

    botCore = TestBotCore(ClientApi(None))
    botCore.setChatDictionary(chat_id, dictionary)

    for i, full_message in enumerate(full_messages):
        response = await botCore.messageProcessing(full_message)
        print(f"=================== Response on message №{i + 1} ======================\n", response)

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
