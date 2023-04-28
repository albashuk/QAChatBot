from __future__ import annotations

from Message import Message
from MessageInterpretation import MessageInterpretation


class QuestionSummary:  # TODO?: rework as Message subclass or save messages separately
    def __init__(self,
                 id: Message.Id,
                 message: str,
                 user_messages_before_question: int,
                 moderator_messages_before_question: int,
                 replies: int = 0,
                 answer_id: Message.Id = None,
                 answer_confidence: float = None,
                 interpretation: MessageInterpretation = None) -> None:
        self.id = id
        self.message = message
        self.messages_before_question = {"user": user_messages_before_question,
                                         "moderator": moderator_messages_before_question}
        self.replies = replies
        self.answer_id = answer_id
        self.answer_confidence = answer_confidence
        self.interpretation = interpretation
