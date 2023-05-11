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


async def process(chat, words, messages):
    botCore = TestBotCore(ClientApi(None))
    dictionary = Dictionary(words)
    botCore.setChatDictionary(chat, dictionary)

    full_messages = [Message(Message.Id(chat, i), message[2], PeerUser(message[0]), None, message[1]) for i, message in enumerate(messages)]

    for i, full_message in enumerate(full_messages):
        response = await botCore.messageProcessing(full_message)
        print(f"=================== Response on message №{i + 1} ======================\n", response)


async def main():
    chat = Chat.Id(PeerChannel(123))
    messages = [
        (1, True, "Hey! Does anyone know where I can find Insulin in Kyiv?"),
        (2, True, "No, sorry, I don't know where to find insulin."),
        (3, True, "Yeh, me too."),
        (4, True, "You can find it at the pharmacy on Zelena Street. This is the only place in Kyiv that is selling insulin."),
        (1, True, "Thanks!"),
        (5, True, "Hello! Don't know where to find Insulin. Could anyone help me, please? That's critical!"),
    ]
    words = {"Ukraine", "Kyiv", "medicament", "Insulin"}
    await process(chat, words, messages)

    chat = Chat.Id(PeerChannel(124))
    messages = [
        (1, True, "Hello! Can I refuel my car at OKKO near Vinnitsa? Can't find a working gas station."),
        (2, True, "Nope, all OKKOs are empty, as all other gas stations... "),
        (3, True, "I'm in a queue for some fuel from 6 a.m. Is it everywhere or am I just so lucky?"),
        (4, True, "Everywhere. So just stay in the queue and hope to get at least a little fuel."),
        (3, True, "Okay, thanks!"),
        (5, True, "Is there a working gas station at Vinnitsa or somewhere nearby? Just need some fuel."),
    ]
    words = {"Ukraine", "Vinnitsa", "OKKO", "fuel", "refuel", "gas", "station", "queue"}
    await process(chat, words, messages)

    # chat = Chat.Id(PeerChannel(125))
    # messages = [
    #     (1, True, "Hey! Does anyone know where I can find Insulin in Kyiv?"),
    #     (2, True, "No, sorry, I don't know where to find insulin."),
    #     (3, True, "Yeh, me too."),
    #     (4, True,
    #      "You can find it at the pharmacy on Zelena Street. This is the only place in Kyiv that is selling insulin."),
    #     (1, True, "Thanks!"),
    #     (5, True, "Hello! Don't know where to find Insulin. Could anyone help me, please? That's critical!"),
    # ]
    # words = {"Ukraine", "Kyiv", "medicament", "Insulin"}
    # await process(chat, words, messages)
    #
    # chat = Chat.Id(PeerChannel(126))
    # messages = [
    #     (1, True, "Hey! Does anyone know where I can find Insulin in Ukraine?"),
    #     (2, True, "No, sorry, I don't know where to find insulin."),
    #     (3, True, "Yeh, me too."),
    #     (4, True,
    #      "You can find it at the pharmacy on Zelena Street. This is the only place in Kyiv that is selling insulin."),
    #     (1, True, "Thanks!"),
    #     (5, True, "Hello! Don't know where to find Insulin. Could anyone help me, please? That's critical!"),
    # ]
    # words = {"Ukraine", "Kyiv", "medicament", "Insulin"}
    # await process(chat, words, messages)


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())


