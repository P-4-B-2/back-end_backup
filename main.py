from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import engine, Base, get_db
from schemas import *
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()



# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Allow your Angular app's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


from seed import seed_database  # Import the seeder function
# Run the seeder
seed_database()

# Create database tables
Base.metadata.create_all(bind=engine)

# CREATE: Add a new question
@app.post("/questions/", response_model=Question)
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    db_question = models.Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

# READ: Get all questions
@app.get("/questions/", response_model=list[Question])
def read_questions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Question).offset(skip).limit(limit).all()

# READ: Get a single question by ID
@app.get("/questions/{question_id}", response_model=Question)
def read_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

# UPDATE: Update a question by ID
@app.put("/questions/{question_id}", response_model=Question)
def update_question(question_id: int, updated_question: QuestionUpdate, db: Session = Depends(get_db)):
    question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    for key, value in updated_question.dict().items():
        setattr(question, key, value)
    db.commit()
    db.refresh(question)
    return question

# DELETE: Delete a question by ID
@app.delete("/questions/{question_id}")
def delete_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    db.delete(question)
    db.commit()
    return {"detail": "Question deleted"}

# CREATE: Add a new conversation
@app.post("/conversations/", response_model=Conversation)
def create_conversation(conversation: ConversationCreate, db: Session = Depends(get_db)):
    # Ensure the bench exists (no need to check for the question anymore)
    db_bench = db.query(models.Bench).filter(models.Bench.id == conversation.bench_id).first()
    if not db_bench:
        raise HTTPException(status_code=404, detail="Bench not found")
    
    # Create the conversation
    db_conversation = models.Conversation(
        startDatetime=conversation.startDatetime,
        bench_id=conversation.bench_id
    )
    
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation
# READ: Get all conversations
@app.get("/conversations/", response_model=list[Conversation])
def read_conversations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Conversation).offset(skip).limit(limit).all()

# CREATE: Add a new answer to a conversation
@app.post("/answers/", response_model=Answer)
def create_answer(answer: AnswerCreate, db: Session = Depends(get_db)):
    # Ensure the conversation and question exist
    db_conversation = db.query(models.Conversation).filter(models.Conversation.id == answer.conversation_id).first()
    db_question = db.query(models.Question).filter(models.Question.id == answer.question_id).first()
    
    if not db_conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    db_answer = models.Answer(**answer.dict())
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer

# READ: Get answers for a specific conversation
@app.get("/conversations/{conversation_id}/answers", response_model=List[Answer])
def get_answers_for_conversation(conversation_id: int, db: Session = Depends(get_db)):
    return db.query(models.Answer).filter(models.Answer.conversation_id == conversation_id).all()

# CREATE: Add a new bench
@app.post("/benches/", response_model=Bench)
def create_bench(bench: BenchCreate, db: Session = Depends(get_db)):
    db_bench = models.Bench(**bench.dict())
    db.add(db_bench)
    db.commit()
    db.refresh(db_bench)
    return db_bench

# READ: Get all benches
@app.get("/benches/", response_model=list[Bench])
def read_benches(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Bench).offset(skip).limit(limit).all()

# READ: Get a single bench by ID
@app.get("/benches/{bench_id}", response_model=Bench)
def read_bench(bench_id: int, db: Session = Depends(get_db)):
    bench = db.query(models.Bench).filter(models.Bench.id == bench_id).first()
    if not bench:
        raise HTTPException(status_code=404, detail="Bench not found")
    return bench

# UPDATE: Update a bench by ID
@app.put("/benches/{bench_id}", response_model=Bench)
def update_bench(bench_id: int, updated_bench: BenchUpdate, db: Session = Depends(get_db)):
    bench = db.query(models.Bench).filter(models.Bench.id == bench_id).first()
    if not bench:
        raise HTTPException(status_code=404, detail="Bench not found")
    for key, value in updated_bench.dict().items():
        setattr(bench, key, value)
    db.commit()
    db.refresh(bench)
    return bench

# DELETE: Delete a bench by ID
@app.delete("/benches/{bench_id}")
def delete_bench(bench_id: int, db: Session = Depends(get_db)):
    bench = db.query(models.Bench).filter(models.Bench.id == bench_id).first()
    if not bench:
        raise HTTPException(status_code=404, detail="Bench not found")
    db.delete(bench)
    db.commit()
    return {"detail": "Bench deleted"}

# UPDATE: Update a conversation by ID
@app.put("/conversations/{conversation_id}", response_model=Conversation)
def update_conversation(
    conversation_id: int, 
    updated_conversation: ConversationUpdate, 
    db: Session = Depends(get_db)
):
    # Check if the conversation exists
    db_conversation = db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()
    
    if not db_conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Update the fields in the conversation object
    for key, value in updated_conversation.dict(exclude_unset=True).items():
        setattr(db_conversation, key, value)
    
    # Commit the changes
    db.commit()
    db.refresh(db_conversation)
    
    return db_conversation

