from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

class QuestionBase(BaseModel):
    text: str
    isActive: bool = True

class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int

    class Config:
        orm_mode = True


class BenchBase(BaseModel):
    name: str

class BenchCreate(BenchBase):
    pass

class BenchUpdate(BenchBase):
    pass

class Bench(BenchBase):
    id: int

    class Config:
        orm_mode = True


class ConversationBase(BaseModel):
    startDatetime: datetime
    endDatetime: Optional[datetime] = None
    sentiment: Optional[int] = None
    summary: Optional[str] = None
    bench_id: int
    question_id: int


class ConversationCreate(ConversationBase):
    pass

class ConversationUpdate(ConversationBase):
    pass

if TYPE_CHECKING:
    from .models import Conversation, Question  # For type checking

class AnswerBase(BaseModel):
    conversation_id: int
    question_id: int
    answer_text: str

class AnswerCreate(AnswerBase):
    pass

class Answer(AnswerBase):
    id: int
    # Instead of including full Conversation and Question objects, use their ids
    question_id: int
    conversation_id: int

    class Config:
        orm_mode = True
        # Use this option to include the 'id' of related models, not the full model
        json_encoders = {
            int: lambda v: v,
        }

    # You can use `exclude` to remove any unwanted fields in the response
    # Optionally, add 'exclude' to avoid including 'conversation' and 'question' entirely in the response

class ConversationBase(BaseModel):
    startDatetime: datetime
    endDatetime: Optional[datetime] = None
    sentiment: Optional[int] = None
    summary: Optional[str] = None
    bench_id: int

class ConversationCreate(BaseModel):
    startDatetime: datetime  # Ensure the name matches the model field
    bench_id: int

    class Config:
        orm_mode = True

class ConversationUpdate(BaseModel):
    startDatetime: Optional[datetime] = None
    endDatetime: Optional[datetime] = None
    sentiment: Optional[int] = None
    summary: Optional[str] = None
    bench_id: Optional[int] = None  # Bench can also be updated if necessary

    class Config:
        orm_mode = True


class Conversation(ConversationBase):
    id: int
    bench_id: int
    answers: List[Answer]  # List of answers linked to this conversation

    class Config:
        orm_mode = True
        json_encoders = {
            int: lambda v: v,
        }
