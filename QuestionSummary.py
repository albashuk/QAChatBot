from __future__ import annotations

from Message import Message


class QuestionSummary:
    def __init__(self,
                 id: Message.Id,
                 user_messages_before_question: int,
                 moderator_messages_before_question: int,
                 replies: int = 0,
                 answer_id: Message.Id = None) -> None:
        self.id = id
        self.messages_before_question = {"user": user_messages_before_question,
                                         "moderator": moderator_messages_before_question}
        self.replies = replies
        self.answer_id = answer_id
