from telethon import TelegramClient, events
from telethon.tl.types import PeerChannel, ReplyInlineMarkup, KeyboardButtonRow, KeyboardButtonCallback

from BotCore import BotCore
from Chat import Chat
from ClientApi import ClientApi
from Message import Message
from TelegramConfig import *

client = TelegramClient("not bot", api_id, api_hash).start()
bot = TelegramClient("bot", api_id, api_hash).start(bot_token=api_token)

botCore = BotCore(ClientApi(client))


@bot.on(events.NewMessage(pattern="/init"))
async def init(event):
    chat_id = Chat.Id(event.peer_id)
    await botCore.initChat(chat_id)


@bot.on(events.NewMessage())
async def message_processing(event):
    if isinstance(event.peer_id, PeerChannel):
        if event.message.message.startswith("/init"):
            return

        message = Message.fromTelethonMessage(event.message)
        response = await botCore.messageProcessing(message)
        if response is not None:
            inline_buttons = ReplyInlineMarkup(
                [
                    KeyboardButtonRow(
                        [
                            KeyboardButtonCallback(
                                text="Yes, thanks!",
                                data=b'Yes'
                            ),
                            KeyboardButtonCallback(
                                text="No. Please call a moderator",
                                data=b'No'
                            )
                        ]
                    )
                ]
            )
            await event.respond(message=response, reply_to=event.message.id, buttons=inline_buttons)


@bot.on(events.CallbackQuery(data=b'Yes'))
async def yes(event):
    await event.respond(message="You're welcome!", reply_to=event.message_id)
    message = Message.fromTelethonMessage(event.get_message())
    await botCore.acceptGeneratedAnswer(message.id, message.reply_id)


@bot.on(events.CallbackQuery(data=b'No'))
async def no(event):
    await event.respond(message="MODERATOR!!!", reply_to=event.message_id)


def main():
    bot.run_until_disconnected()


if __name__ == "__main__":
    main()
