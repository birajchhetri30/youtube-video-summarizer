from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_pipeline import get_bedrock_client, run_rag_pipeline, get_transcript, extract_video_id, get_or_create_summary, get_video_title
import os
from typing import List

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
    urls: List[str]
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
    video_ids = []
    transcripts = []
    for url in data.urls:
        video_id = extract_video_id(url)
        if not video_id:
            raise HTTPException(status_code=400, detail=f"Invalid URL: {url}")
        video_ids.append(video_id)
    
    if len(video_ids) > 3:
        raise HTTPException(status_code=400, detail="Maximum 3 videos allowed per request")
    
    # Sort video_ids for consistent combined_id
    combined_id = "_".join(sorted(video_ids))
    
    combined_transcript = ""
    for i, (url, video_id) in enumerate(zip(data.urls, video_ids)):
        try:
            transcript = get_transcript(video_id, url)
            title = get_video_title(video_id)
            transcripts.append(transcript)
            combined_transcript += f"\n\n--- Video {i+1}: {title} ({url}) ---\n{transcript}"
        except TranscriptsDisabled:
            raise HTTPException(
                status_code=400,
                detail=f"Transcripts are disabled for video: {url}"
            )
        except NoTranscriptFound:
            raise HTTPException(
                status_code=400,
                detail=f"No transcript available for video: {url}"
            )
        except VideoUnavailable:
            raise HTTPException(
                status_code=404,
                detail=f"YouTube video is unavailable: {url}"
            )

    try:
        qa_chain, summary_chain = run_rag_pipeline(
            combined_id,
            combined_transcript,
            bedrock_client
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initialize RAG pipeline: {str(e)}"
        )

    # Run summary
    try:
        summary = get_or_create_summary(combined_id, summary_chain, combined_transcript)
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
