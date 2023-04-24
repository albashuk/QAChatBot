import logging

import torch

from BERT import BERT
from Chat import Chat
from ClientApi import ClientApi
from Message import Message
from QuestionDetection import QuestionDetection
from QuestionSummary import QuestionSummary
from properties import properties


class BotCore:
    # logs
    __log = logging.getLogger('__name__')

    # modules
    __device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    __bert = BERT(__device)
    __questionDetection = QuestionDetection(__device, __bert)

    # data
    __chats = {}  # TODO: use database
    __dictionaries = {}  # TODO: use database

    def __init__(self, clientApi: ClientApi) -> None:
        self.__clientApi = clientApi

    def messageProcessing(self, message: Message, with_answering: bool = True):
        chat = self.__chatFromMessage(message)
        user_type = "moderator" if self.__clientApi.isFromModerator(message) else "user"
        chat.message_count[user_type] += 1
        while len(chat.questions_queue[user_type]) > 0 and \
                chat.questions_queue[user_type][0].messages_before_question[user_type] \
                + properties.max_answers[user_type] \
                < chat.message_count[user_type]:
            chat.questions_queue[user_type].popleft()

        if self.__isQuestion(message):
            questionSummary = QuestionSummary(message.id, chat.message_count["user"], chat.message_count["moderator"])
            chat.questions_queue["user"].append(questionSummary)
            chat.questions_queue["moderator"].append(questionSummary)
            chat.questions[message.id] = questionSummary

            if with_answering:
                pass  # TODO: realize
        else:
            if message.reply_id is not None:
                reply = chat.questions.get(message.reply_id)
                if reply is not None and isinstance(reply, QuestionSummary):
                    reply.replies += 1
                    if reply.replies <= properties.max_replies:
                        self.__answerChecking(reply, message, self.__messageWeight(user_type, True))

            for question in chat.questions_queue[user_type]:
                self.__answerChecking(question, message, self.__messageWeight(user_type))

        # TODO: dictionary updating

    def initChatQuestions(self, chat: Chat):
        if not self.__clientApi.hasAccessToChatHistory(chat):
            self.__log.warning(f"Client hasn't access to chat ({chat.id})_ history")
            return

    @classmethod
    def __chatFromMessage(cls, message: Message):
        if cls.__chats.get(message.id.chat_id) is None:
            cls.__chats[message.id.chat_id] = Chat(message.id.chat_id)
        return cls.__chats[message.id.chat_id]

    @classmethod
    def __isQuestion(cls, message: Message) -> bool:
        if message.is_question is None:
            message.is_question = cls.__questionDetection.isQuestion(message.message)
        return message.is_question

    @classmethod
    def __answerChecking(cls, question: QuestionSummary, answer: Message, weight: float = 0):
        pass  # TODO: realize

    @staticmethod
    def __messageWeight(user_type: str, reply: bool = False) -> float:
        if reply:
            return properties.user_weight[user_type] * properties.reply_weight
        else:
            return properties.user_weight[user_type]




# debuging

# botCore = BotCore(None)
# message = Message(None, "I'm writing a letter to you", None)
# print(botCore.isQuestion(message))