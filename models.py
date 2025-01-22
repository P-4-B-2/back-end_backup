from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    isActive = Column(Boolean, default=True)

    # Relationship with Answer table
    answers = relationship("Answer", back_populates="question")


class Bench(Base):
    __tablename__ = "benches"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # Relationship to Conversation
    conversations = relationship("Conversation", back_populates="bench")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    startDatetime = Column(DateTime, nullable=False)
    endDatetime = Column(DateTime, nullable=True)
    sentiment = Column(Integer, nullable=True)
    summary = Column(String, nullable=True)
    bench_id = Column(Integer, ForeignKey("benches.id"))
    bench = relationship("Bench", back_populates="conversations")

    # Relationship to Answer table
    answers = relationship("Answer", back_populates="conversation")


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    answer_text = Column(String, nullable=False)

    # Relationships
    conversation = relationship("Conversation", back_populates="answers")
    question = relationship("Question", back_populates="answers")
