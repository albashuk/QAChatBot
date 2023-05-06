import logging

import torch

from BertWrapper import BertWrapper
from Chat import Chat
from ClientApi import ClientApi
from Dictionary import Dictionary
from Message import Message
from MessageInterpretation import MessageInterpretation
from MessageInterpretationService import MessageInterpretationService
from QuestionDetection import QuestionDetection
from QuestionSummary import QuestionSummary
from parser import parseOnWords
from properties import properties


class BotCore:
    # logs
    __log = logging.getLogger('__name__')

    # modules
    __device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    __bert = BertWrapper(__device)
    __questionDetection = QuestionDetection(__device, __bert)
    __messageInterpretationService = MessageInterpretationService(__device, __bert)

    # data
    __chats = {}  # TODO: use database

    def __init__(self, clientApi: ClientApi) -> None:
        self.__clientApi = clientApi

    async def messageProcessing(self, message: Message, with_answering: bool = True):
        chat = self.__chatFromMessage(message.id)
        user_type = "moderator" if await self.__clientApi.isFromModerator(message) else "user"
        chat.message_count[user_type] += 1
        while len(chat.questions_queue[user_type]) > 0 \
                and not chat.questions_queue[user_type][0].waitingForAnswer(chat.message_count[user_type], user_type):
            chat.questions_queue[user_type].popleft()

        self.__updateDictionary(message)

        if self.__isQuestion(message):
            question = QuestionSummary(message.id,
                                              message.message,
                                              chat.message_count["user"],
                                              chat.message_count["moderator"])
            chat.questions_queue["user"].append(question)
            chat.questions_queue["moderator"].append(question)
            chat.questions[message.id] = question

            if with_answering:
                answers = []
                for oldQuestionId in list(chat.questions)[:-1]:
                    oldQuestion = chat.questions[oldQuestionId]
                    if oldQuestion.answer_id is not None:
                        similarity = self.__questionSimilarity(question, oldQuestion)
                        if similarity >= properties.question_similarity_threshold:
                            answers.append((similarity * oldQuestion.answer_confidence, oldQuestion.answer_id))
                    else:
                        if not oldQuestion.waitingForReply() \
                                and not oldQuestion.waitingForAnswer(chat.message_count["user"], "user") \
                                and not oldQuestion.waitingForAnswer(chat.message_count["moderator"], "moderator"):
                            chat.questions.pop(oldQuestionId)

                top_answers = sorted(answers)[:properties.top_answers_max_size]
                return self.__clientApi.buildRespond(top_answers) if len(top_answers) != 0 else None
        else:
            if message.reply_id is not None:
                reply = chat.questions.get(message.reply_id)
                if reply is not None and isinstance(reply, QuestionSummary):
                    reply.replies += 1
                    if reply.replies <= properties.max_replies:
                        self.__answerChecking(reply, message, self.__messageWeight(user_type, True))

            for question in chat.questions_queue[user_type]:
                self.__answerChecking(question, message, self.__messageWeight(user_type))

    async def acceptGeneratedAnswer(self, answer_id: Message.Id, question_id: Message.Id):
        chat = self.__chatFromMessage(answer_id)
        question = chat.questions[question_id]
        question.answer_id = answer_id
        question.answer_confidence = 1

    async def initChat(self, chat_id: Chat.Id):
        if self.__chats.get(chat_id) is not None:
            self.__log.warning(f"Chat ({chat_id.value()}) is already init")
            return
        self.__chats[chat_id] = Chat(chat_id, Dictionary(None, True, True))

        if not self.__clientApi.hasAccessToChatHistory(chat_id):
            self.__log.warning(f"Client hasn't access to chat ({chat_id.value()}) history")
            return

        try:
            chatIter = await self.__clientApi.buildIter(chat_id, properties.history_limit)
            while True:
                message = await chatIter.next()
                await self.messageProcessing(message, False)
        except StopAsyncIteration:
            pass

    @classmethod
    def __chatFromMessage(cls, message_id: Message.Id):
        if cls.__chats.get(message_id.chat_id) is None:
            cls.__chats[message_id.chat_id] = Chat(message_id.chat_id, Dictionary(None, True, True))
        return cls.__chats[message_id.chat_id]

    @classmethod
    def __isQuestion(cls, message: Message) -> bool:  # TODO: check separate sentences
        if message.is_question is None:
            message.is_question = cls.__questionDetection.isQuestion(message.message)
        return message.is_question

    @classmethod
    def __questionSimilarity(cls, question1: QuestionSummary, question2: QuestionSummary):
        return cls.__messageInterpretationService.similarity(cls.__messageInterpretation(question1),
                                                             cls.__messageInterpretation(question2),
                                                             0.7)  # TODO: config coefficient

    @classmethod
    def __answerChecking(cls, question: QuestionSummary, answer: Message, weight: float = 0):
        similarity = cls.__messageInterpretationService.similarity(cls.__messageInterpretation(question),
                                                                   cls.__messageInterpretation(answer),
                                                                   0.4)  # TODO: config coefficient
        answer_confidence = similarity * weight  # TODO: improve formula
        if similarity >= properties.qa_similarity_threshold and answer_confidence >= properties.answer_threshold:
            if question.answer_id is None or question.answer_confidence < answer_confidence:
                question.answer_id = answer.id
                question.answer_confidence = answer_confidence

    @classmethod
    def __messageInterpretation(cls, message: Message | QuestionSummary) -> MessageInterpretation:
        chat = cls.__chatFromMessage(message.id)
        if message.interpretation is None or message.interpretation.dict_ver != chat.dictionary.getVersion():
            message.interpretation = cls.__messageInterpretationService.toInterpretation(message.message,
                                                                                         chat.dictionary)
        return message.interpretation

    @classmethod
    def __updateDictionary(cls, message: Message):
        chat = cls.__chatFromMessage(message.id)
        words = parseOnWords(message.message)
        for word in words:
            chat.dictionary.increaseWordCurrency(word)
        if (chat.message_count["user"] + chat.message_count["moderator"]) % 1000 == 0:
            chat.dictionary.cleanCurrency()
            chat.dictionary.update()

    @staticmethod
    def __messageWeight(user_type: str, reply: bool = False) -> float:
        if reply:
            return properties.user_weight[user_type] * properties.reply_weight
        else:
            return properties.user_weight[user_type]




# debugging

# botCore = BotCore(None)
# message = Message(None, "I'm writing a letter to you", None)
# print(botCore.isQuestion(message))
