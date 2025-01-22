from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
import models
from datetime import datetime

# Seed data
questions = [
    {"text": "What is your opinion on the new product?", "isActive": True},
    {"text": "How do you feel about our customer support?", "isActive": True},
    {"text": "Would you recommend our services?", "isActive": False}
]

benches = [
    {"name": "Bench 1"},
    {"name": "Bench 2"}
]

# Remove 'question_id' from conversations
conversations = [
    {"startDatetime": datetime(2025, 1, 22, 10, 0), "endDatetime": datetime(2025, 1, 22, 11, 0), "sentiment": 5, "summary": "Great conversation.", "bench_id": 1},
    {"startDatetime": datetime(2025, 1, 22, 12, 0), "endDatetime": datetime(2025, 1, 22, 13, 0), "sentiment": 4, "summary": "Productive discussion.", "bench_id": 2},
]

answers = [
    (1, 1, "Yes, I like the product."),
    (1, 2, "The support team is quite helpful."),
    (2, 1, "The product is okay, but could be improved."),
    (2, 3, "I would recommend it to others."),
]

def seed_database():
    # Create all tables
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        # Seed questions
        if db.query(models.Question).first() is None:
            print("Seeding questions...")
            for question in questions:
                db.add(models.Question(**question))
            db.commit()

        # Seed benches
        if db.query(models.Bench).first() is None:
            print("Seeding benches...")
            for bench in benches:
                db.add(models.Bench(**bench))
            db.commit()

        # Seed conversations
        if db.query(models.Conversation).first() is None:
            print("Seeding conversations...")
            for conversation in conversations:
                db_conversation = models.Conversation(
                    startDatetime=conversation["startDatetime"],
                    endDatetime=conversation["endDatetime"],
                    sentiment=conversation["sentiment"],
                    summary=conversation["summary"],
                    bench_id=conversation["bench_id"],
                )
                db.add(db_conversation)
            db.commit()

        # Seed answers (link conversations with questions)
        if db.query(models.Answer).first() is None:
            print("Seeding answers...")
            for conversation_id, question_id, answer_text in answers:
                db.add(models.Answer(conversation_id=conversation_id, question_id=question_id, answer_text=answer_text))
            db.commit()

        print("Database seeded successfully.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
