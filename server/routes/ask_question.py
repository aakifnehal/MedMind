from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from modules.llm import get_llm_chain
from modules.query_handler import query_chain
from langchain_core.documents import Document
from langchain.schema import BaseRetriever
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone
from pydantic import Field
from typing import List, Optional
from logger import logger
import os
from dotenv import load_dotenv

load_dotenv()

router=APIRouter()

@router.post("/ask/")
async def ask_question(question: str = Form(...)):
    try:
        logger.info(f"user query: {question}")

        # Embed model + Pinecone setup
        PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
        PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "medmind-index")
        
        pc = Pinecone(api_key=PINECONE_API_KEY)
        index = pc.Index(PINECONE_INDEX_NAME)
        embed_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        
        embedded_query = embed_model.embed_query(question)
        res = index.query(vector=embedded_query, top_k=3, include_metadata=True)

        logger.debug(f"Pinecone query results: {len(res['matches'])} matches found")
        
        docs = []
        for match in res["matches"]:
            # Get text from metadata where we stored it
            text_content = match["metadata"].get("text", "")
            if text_content:  # Only add docs with actual content
                doc = Document(
                    page_content=text_content,
                    metadata=match["metadata"]
                )
                docs.append(doc)
        
        logger.debug(f"Created {len(docs)} documents for retrieval")
        
        if not docs:
            return {
                "response": "I couldn't find any relevant information in the uploaded documents. Please make sure documents are uploaded and processed correctly.",
                "sources": []
            }

        class SimpleRetriever(BaseRetriever):
            tags: Optional[List[str]] = Field(default_factory=list)
            metadata: Optional[dict] = Field(default_factory=dict)

            def __init__(self, documents: List[Document]):
                super().__init__()
                self._docs = documents

            def _get_relevant_documents(self, query: str) -> List[Document]:
                return self._docs

        retriever = SimpleRetriever(docs)
        chain = get_llm_chain(retriever)
        result = query_chain(chain, question)

        logger.info("query successful")
        return result

    except Exception as e:
        logger.exception("Error processing question")
        return JSONResponse(status_code=500, content={"error": str(e)})