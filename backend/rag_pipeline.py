from youtube_transcript_api import YouTubeTranscriptApi
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_aws import ChatBedrock, BedrockEmbeddings
from langchain_chroma import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
import boto3
import os


VECTORSTORE_DIR = "vectorstore"

def get_vectorstore(video_id, chunks, embeddings):
    persist_path = os.path.join(VECTORSTORE_DIR, video_id)

    if os.path.exists(persist_path):
        print(f"Loading existing vectorstore for {video_id}")
        db = Chroma(
            persist_directory=persist_path,
            embedding_function=embeddings
        )
        # Check if the vectorstore has documents
        if len(db.get()['ids']) == 0:
            print(f"Vectorstore is empty, recreating for {video_id}")
            db = Chroma.from_documents(
                documents=chunks,
                embedding=embeddings,
                persist_directory=persist_path
            )
        return db

    print(f"Creating vectorstore for {video_id}")
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_path
    )
    return db

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# ---------- AWS Bedrock Client ----------
def get_bedrock_client(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, AWS_REGION):
    return boto3.client(
        service_name="bedrock-runtime",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_session_token=AWS_SESSION_TOKEN,
    )


def get_llm(bedrock_client, model="amazon.nova-lite-v1:0", temperature=0):
    return ChatBedrock(client=bedrock_client, model_id=model, temperature=temperature)


# ---------- YouTube Transcript ----------
def extract_video_id(url: str):
    if "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return url


def get_transcript(video_id: str, url: str):
    os.makedirs(VECTORSTORE_DIR, exist_ok=True)

    video_dir = os.path.join(VECTORSTORE_DIR, video_id)
    os.makedirs(video_dir, exist_ok=True)

    path = os.path.join(video_dir, "transcript.txt")

    if os.path.exists(path):
        print(f"Loading cached transcript for {video_id}")
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    transcript_obj = YouTubeTranscriptApi().fetch(video_id)
    text = " ".join([s.text for s in transcript_obj.snippets])

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

    return text


def get_or_create_summary(video_id, summary_chain, transcript):
    path = os.path.join(VECTORSTORE_DIR, video_id, "summary.txt")

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    summary = summary_chain.invoke({"transcript": transcript})

    with open(path, "w", encoding="utf-8") as f:
        f.write(summary)

    return summary


# ---------- RAG + Summary ----------
def run_rag_pipeline(video_id, transcript_text, bedrock_client):
    # Create document
    docs = [Document(page_content=transcript_text)]

    # Split
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(docs)

    # Embeddings
    embeddings = BedrockEmbeddings(
        client=bedrock_client,
        model_id="amazon.titan-embed-text-v2:0"
    )

    # Persisted Vector DB
    db = get_vectorstore(video_id, chunks, embeddings)
    retriever = db.as_retriever()

    # QA Chain
    qa_prompt = PromptTemplate(
        template="""You are a helpful AI assistant.
Use ONLY the following transcript excerpts to answer the question.
If not found, say "I don't know based on the transcript."

Transcript:
{context}

Question:
{question}

Answer:""",
        input_variables=["context", "question"]
    )

    qa_chain = (
            {
                "context": retriever | RunnableLambda(format_docs),
                "question": RunnablePassthrough(),
            }
            | qa_prompt
            | get_llm(bedrock_client)
            | StrOutputParser()
    )

    # Summary Chain
    summary_prompt = PromptTemplate(
        template="""Summarize the following YouTube transcript into clear bullet-point key insights.

Transcript:
{transcript}

Summary:""",
        input_variables=["transcript"],
    )

    summary_chain = (
            summary_prompt
            | get_llm(bedrock_client)
            | StrOutputParser()
    )

    return qa_chain, summary_chain
