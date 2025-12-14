from youtube_transcript_api import YouTubeTranscriptApi
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_aws import ChatBedrock, BedrockEmbeddings
from langchain_chroma import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import boto3


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


def get_transcript(url: str):
    video_id = extract_video_id(url)
    transcript_obj = YouTubeTranscriptApi().fetch(video_id)
    full_text = " ".join([snippet.text for snippet in transcript_obj.snippets])
    return full_text


# ---------- RAG + Summary ----------
def run_rag_pipeline(transcript_text, bedrock_client):
    # Create document
    docs = [Document(page_content=transcript_text)]

    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = text_splitter.split_documents(docs)

    # Embeddings + Chroma
    embeddings = BedrockEmbeddings(client=bedrock_client, model_id="amazon.titan-embed-text-v2:0")
    db = Chroma.from_documents(documents=chunks, embedding=embeddings)
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
                "context": retriever,
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
