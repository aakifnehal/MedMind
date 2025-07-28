"""
Test script to debug MedMind issues
"""
import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

def test_pinecone_connection():
    try:
        PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
        PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "medmind-index")
        
        if not PINECONE_API_KEY:
            print("❌ PINECONE_API_KEY not found in environment variables")
            return False
        
        pc = Pinecone(api_key=PINECONE_API_KEY)
        
        # Check if index exists
        indexes = [i["name"] for i in pc.list_indexes()]
        print(f"📋 Available indexes: {indexes}")
        
        if PINECONE_INDEX_NAME not in indexes:
            print(f"❌ Index '{PINECONE_INDEX_NAME}' not found")
            return False
        
        # Get index stats
        index = pc.Index(PINECONE_INDEX_NAME)
        stats = index.describe_index_stats()
        print(f"📊 Index stats: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error connecting to Pinecone: {e}")
        return False

def test_google_ai():
    try:
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        if not GOOGLE_API_KEY:
            print("❌ GOOGLE_API_KEY not found in environment variables")
            return False
        
        embed_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        test_embedding = embed_model.embed_query("test query")
        print(f"✅ Google AI embeddings working, dimension: {len(test_embedding)}")
        return True
        
    except Exception as e:
        print(f"❌ Error with Google AI: {e}")
        return False

def test_groq():
    try:
        from langchain_groq import ChatGroq
        
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        if not GROQ_API_KEY:
            print("❌ GROQ_API_KEY not found in environment variables")
            return False
        
        llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama3-70b-8192")
        print("✅ Groq LLM connection successful")
        return True
        
    except Exception as e:
        print(f"❌ Error with Groq: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing MedMind Components...")
    print("=" * 50)
    
    print("\n1. Testing Pinecone Connection...")
    test_pinecone_connection()
    
    print("\n2. Testing Google AI Embeddings...")
    test_google_ai()
    
    print("\n3. Testing Groq LLM...")
    test_groq()
    
    print("\n✅ Testing complete!")
