from fastapi import FastAPI
from pydantic import BaseModel
from rag_pipeline import get_bedrock_client, run_rag_pipeline, get_transcript
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # allow POST, OPTIONS, etc.
    allow_headers=["*"],
)

# --------- Request Body ---------
class RequestBody(BaseModel):
    url: str
    question: str = None


# --------- Initialize Bedrock client ---------
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.environ.get("AWS_SESSION_TOKEN")
AWS_REGION = os.environ.get("AWS_REGION")

bedrock_client = get_bedrock_client(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, AWS_REGION)


# --------- API Endpoint ---------
@app.post("/process")
async def process_video(data: RequestBody):
    transcript = get_transcript(data.url)

    qa_chain, summary_chain = run_rag_pipeline(transcript, bedrock_client)

    # Run summary
    summary = summary_chain.invoke({"transcript": transcript})

    # Run Q&A if question is provided
    answer = None
    if data.question:
        answer = qa_chain.invoke(data.question)

    return {
        "summary": summary,
        "answer": answer
    }
