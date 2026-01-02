from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_pipeline import get_bedrock_client, run_rag_pipeline, get_transcript, extract_video_id, get_or_create_summary
import os

from youtube_transcript_api import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable
)

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
    video_id = extract_video_id(data.url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid URL")

    try:
        transcript = get_transcript(video_id, data.url)
    except TranscriptsDisabled:
        raise HTTPException(
            status_code=400,
            detail="Transcripts are disabled for this video"
        )
    except NoTranscriptFound:
        raise HTTPException(
            status_code=400,
            detail="No transcript available for this video"
        )
    except VideoUnavailable:
        raise HTTPException(
            status_code=404,
            detail="YouTube video is unavailable"
        )

    try:
        qa_chain, summary_chain = run_rag_pipeline(
            video_id,
            transcript,
            bedrock_client
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initialize RAG pipeline: {str(e)}"
        )

    # Run summary
    try:
        summary = get_or_create_summary(video_id, summary_chain, transcript)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate summary: {str(e)}"
        )

    # Run Q&A if question is provided
    try:
        answer = None
        if data.question:
            answer = qa_chain.invoke(data.question)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate answer: {str(e)}"
        )

    return {
        "summary": summary,
        "answer": answer
    }
