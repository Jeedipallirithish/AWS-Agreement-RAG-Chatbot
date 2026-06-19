from fastapi import FastAPI
from pydantic import BaseModel
import time
from database import log_query
from ingest import ingest_pdf
from rag_pipeline import ask_question
from database import get_analytics
app = FastAPI()

class QuestionRequest(BaseModel):
    question: str


@app.post("/ingest")
def ingest():

    ingest_pdf(
        "AWS Customer Agreement.pdf"
    )

    return {
        "message": "PDF Ingested Successfully"
    }






@app.post("/ask")
def ask(data: QuestionRequest):

    start = time.time()

    answer, docs = ask_question(
        data.question
    )

    latency = time.time() - start

    answer_found = (
        0 if "I could not find" in answer
        else 1
    )

    log_query(
        data.question,
        answer_found,
        latency
    )

    sources = [
        doc.page_content[:300]
        for doc in docs
    ]

    return {
        "answer": answer,
        "sources": sources
    }

@app.get("/")
def home():
    return {
        "message":"AWS Agreement RAG API Running"
    }



@app.get("/analytics")
def analytics():

    return get_analytics()