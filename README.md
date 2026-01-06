# 🎥 YouTube Transcript Summarizer and Q&A

A full-stack **Retrieval-Augmented Generation (RAG)** application that transforms YouTube videos into an interactive, searchable knowledge source. The system extracts video transcripts, generates concise summaries with titles, and enables users to ask transcript-grounded questions across multiple videos using **AWS Bedrock** and **LangChain**.

---

## 🚀 Features

- 📄 Automatic YouTube transcript extraction (up to 3 videos)
- 📌 Bullet-point summarization with video titles
- ❓ Context-aware question answering across multiple videos
- 🧠 Retrieval-Augmented Generation (RAG) with combined knowledge base
- ☁️ Powered by AWS Bedrock LLMs
- ⚡ FastAPI backend & Next.js frontend

---

## 🧠 How It Works

1. User submits up to 3 YouTube video URLs
2. The backend extracts transcripts and titles for each video
3. Transcripts are combined into a single knowledge base
4. The combined content is split into chunks and embedded
5. Embeddings are stored in a vector database (Chroma)
6. A summary of all videos is generated, including titles
7. For Q&A:
   - Relevant transcript chunks are retrieved from the combined base
   - The LLM generates answers grounded in the transcripts of all videos

---

## 🛠 Tech Stack

### Backend
- Python
- FastAPI
- YouTube Transcript API
- LangChain (LCEL)
- AWS Bedrock
  - `amazon.nova-lite-v1` (LLM)
  - `amazon.titan-embed-text-v2` (Embeddings)
- ChromaDB
- boto3
- python-dotenv

### Frontend
- Next.js (App Router)
- React
- TypeScript

---

## ⚙️ Setup Instructions

### 1. Backend Setup

Create a `.env` file:
```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_SESSION_TOKEN=your_session_token
AWS_REGION=your_aws_region
```

Run the backend:
```
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
```
Backend will be available at ```http://localhost:8000```

### 2. Frontend Setup

Run the frontend:
```
cd frontend
npm install
npm run dev
```

---

## 🔌 API Endpoint

### POST `/process`

**Request Body**
```
{
  "urls": ["https://www.youtube.com/watch?v=VIDEO_ID1", "https://www.youtube.com/watch?v=VIDEO_ID2"],
  "question": "optional question about the videos"
}
```

**Notes:**
- Supports up to 3 YouTube URLs in the `urls` array.
- Summaries include video titles for each video.
- Q&A answers can draw from the combined knowledge of all provided videos.

### Response
```
{
  "summary": "Bullet-point summary with titles and key insights from all videos",
  "answer": "answer to the question (if provided)"
}
```