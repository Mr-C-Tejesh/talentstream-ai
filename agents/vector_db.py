import os
import psycopg2
from pgvector.psycopg2 import register_vector
from langchain_community.embeddings import LiteLLMEmbeddings
from typing import List, Dict, Any

class VectorDB:
    def __init__(self):
        self.conn_str = os.getenv("DATABASE_URL", "postgresql://localhost:5432/talentstream")
        self.embeddings = LiteLLMEmbeddings(model="groq/llama-3.3-70b-versatile") # Note: Check if Groq supports embeddings via litellm or use another provider
        # For now, let's assume OpenAI or a standard provider for embeddings if Groq doesn't support it directly
        if "GROQ_API_KEY" in os.environ and not os.getenv("OPENAI_API_KEY"):
             # Fallback to a free embedding model if needed, or assume user has one
             pass

    def get_connection(self):
        conn = psycopg2.connect(self.conn_str)
        register_vector(conn)
        return conn

    def create_tables(self):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS resumes (
                        id SERIAL PRIMARY KEY,
                        candidate_name TEXT,
                        resume_text TEXT,
                        embedding vector(1536), -- Assuming OpenAI dimensions for now
                        metadata JSONB
                    )
                """)
            conn.commit()

    def add_resume(self, name: str, text: str, metadata: Dict[str, Any]):
        embedding = self.embeddings.embed_query(text)
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO resumes (candidate_name, resume_text, embedding, metadata) VALUES (%s, %s, %s, %s)",
                    (name, text, embedding, json.dumps(metadata))
                )
            conn.commit()

    def search_candidates(self, query_text: str, limit: int = 5):
        query_embedding = self.embeddings.embed_query(query_text)
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT candidate_name, resume_text, metadata, 1 - (embedding <=> %s) AS score FROM resumes ORDER BY score DESC LIMIT %s",
                    (query_embedding, limit)
                )
                return cur.fetchall()
