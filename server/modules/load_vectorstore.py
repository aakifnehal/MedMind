import os
import time
from pathlib import Path
from dotenv import load_dotenv
from tqdm.auto import tqdm
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = "us-east-1"
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "medmind-index")

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

UPLOAD_DIR = "./uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
spec = ServerlessSpec(cloud="aws", region=PINECONE_ENV)
existing_indexes = [i["name"]for i in pc.list_indexes()]

if PINECONE_INDEX_NAME not in existing_indexes:
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=768,  # Google GenAI's embedding 001 model returns 768-dimensional vectors
        metric="dotproduct",
        spec=spec
    )
    while not pc.describe_index(PINECONE_INDEX_NAME).status.ready:
        print("Waiting for Pinecone index to be ready...")
        time.sleep(1)

index = pc.Index(PINECONE_INDEX_NAME)


# Load, Split, Embed and Upsert PDF Document contents

def load_vectorstore(uploaded_files):
    embed_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    file_paths = []

    # 1. Upload
    for file in uploaded_files:
        save_path = Path(UPLOAD_DIR)/file.filename
        with open(save_path, "wb") as f:
            f.write(file.file.read())
        file_paths.append(str(save_path))
        print(f"Saved file: {save_path}")

    # 2. Load and Split
    for file_path in file_paths:
        print(f"Processing file: {file_path}")
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        print(f"Loaded {len(documents)} pages from {file_path}")

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = splitter.split_documents(documents)
        print(f"Split into {len(chunks)} chunks")

        # for showing the chunks to the user
        texts = [chunk.page_content for chunk in chunks]
        
        # Create metadata with text content and source info
        metadata = []
        for i, chunk in enumerate(chunks):
            meta = chunk.metadata.copy()
            meta["text"] = chunk.page_content  # Store the actual text content
            meta["source"] = Path(file_path).name  # Store the filename as source
            meta["chunk_id"] = i
            metadata.append(meta)
            
        ids = [f"{Path(file_path).stem}-{i}" for i in range(len(chunks))]

        # 3. Embeding
        print(f"Embedding {len(chunks)} chunks from {file_path}...")
        embeddings = embed_model.embed_documents(texts)
        print(f"Generated {len(embeddings)} embeddings")

        # 4. Upserting
        print(f"Upserting {len(chunks)} chunks to Pinecone index...")
        with tqdm(total=len(embeddings), desc="Upserting to Pinecone") as progress:
            # Create vectors with proper format: (id, embedding, metadata)
            vectors = list(zip(ids, embeddings, metadata))
            index.upsert(vectors=vectors)
            progress.update(len(embeddings))

        print(f"Successfully processed {file_path} with {len(chunks)} chunks.")
        



