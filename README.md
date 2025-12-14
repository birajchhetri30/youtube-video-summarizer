# 🎥 YouTube Transcript RAG Application

A full-stack **Retrieval-Augmented Generation (RAG)** application that transforms YouTube videos into an interactive, searchable knowledge source. The system extracts video transcripts, generates concise summaries, and enables users to ask transcript-grounded questions using **AWS Bedrock** and **LangChain**.

---

## 🚀 Features

- 📄 Automatic YouTube transcript extraction
- 📌 Bullet-point summarization of video content
- ❓ Context-aware question answering
- 🧠 Retrieval-Augmented Generation (RAG)
- ☁️ Powered by AWS Bedrock LLMs
- ⚡ FastAPI backend & Next.js frontend

---

## 🧠 How It Works

1. User submits a YouTube video URL
2. The backend extracts the video transcript
3. The transcript is split into chunks and embedded
4. Embeddings are stored in a vector database (Chroma)
5. For Q&A:
   - Relevant transcript chunks are retrieved
   - The LLM generates answers grounded strictly in the transcript
6. A summary of the full transcript is generated in parallel

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