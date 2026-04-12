import os
import json
import psycopg2
from pgvector.psycopg2 import register_vector
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List, Dict, Any

class VectorDB:
    def __init__(self):
        # Default to local postgres if no URL is provided
        self.conn_str = os.getenv("DATABASE_URL", "postgresql://localhost:5432/talentstream")
        
        # If it's a remote DB (like Supabase), we often need SSL
        if "localhost" not in self.conn_str and "sslmode" not in self.conn_str:
            if "?" in self.conn_str:
                self.conn_str += "&sslmode=require"
            else:
                self.conn_str += "?sslmode=require"
        
        # Using HuggingFace (Local & 100% Free)
        self.model_name = "all-MiniLM-L6-v2"
        print(f"📡 Loading local embedding model ({self.model_name})...")
        self.embeddings = HuggingFaceEmbeddings(model_name=self.model_name)

    def get_connection(self, register=True):
        """Get a connection, optionally registering pgvector."""
        try:
            conn = psycopg2.connect(self.conn_str)
            if register:
                try:
                    register_vector(conn)
                except psycopg2.Error as e:
                    if "type \"vector\" does not exist" in str(e):
                        pass
                    else:
                        raise e
            return conn
        except Exception as e:
            print(f"❌ Database Connection Error: {e}")
            return None

    def initialize_db(self, reset=False):
        """Create extension and resumes table if they don't exist."""
        conn = self.get_connection(register=False)
        if not conn: return False
        
        try:
            with conn.cursor() as cur:
                print("🛠️ Enabling pgvector extension...")
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
                conn.commit()
                
                # Now that extension is guaranteed, register it for this connection
                register_vector(conn)
                
                if reset:
                    print("⚠️ Resetting resumes table...")
                    cur.execute("DROP TABLE IF EXISTS resumes CASCADE")
                    conn.commit()

                print("🛠️ Creating resumes table (384 dimensions for local model)...")
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS resumes (
                        id SERIAL PRIMARY KEY,
                        candidate_name TEXT NOT NULL,
                        resume_text TEXT NOT NULL,
                        embedding vector(384),
                        metadata JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                print("🛠️ Creating HNSW index...")
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS resumes_embedding_idx ON resumes 
                    USING hnsw (embedding vector_cosine_ops);
                """)
            conn.commit()
            print("✅ Vector DB Initialized Successfully.")
            return True
        except Exception as e:
            print(f"❌ DB Initialization Error: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def add_resume(self, name: str, text: str, metadata: Dict[str, Any] = None):
        """Embeds and adds a resume to the database."""
        conn = self.get_connection()
        if not conn: return False

        try:
            print(f"🧠 Generating local embedding for {name}...")
            embedding = self.embeddings.embed_query(text)
            
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO resumes (candidate_name, resume_text, embedding, metadata) VALUES (%s, %s, %s, %s)",
                    (name, text, embedding, json.dumps(metadata or {}))
                )
            conn.commit()
            print(f"✅ Added {name} to Vector DB.")
            return True
        except Exception as e:
            print(f"❌ Error adding resume: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def search_candidates(self, query_text: str, limit: int = 5):
        """Performs semantic search to find top candidates."""
        conn = self.get_connection()
        if not conn: return []

        try:
            print(f"🔍 Searching for: {query_text}...")
            query_embedding = self.embeddings.embed_query(query_text)
            with conn.cursor() as cur:
                # Using cosine distance (<=>) with explicit vector cast
                cur.execute(
                    "SELECT candidate_name, resume_text, metadata, 1 - (embedding <=> %s::vector) AS score FROM resumes ORDER BY score DESC LIMIT %s",
                    (query_embedding, limit)
                )
                return cur.fetchall()
        except Exception as e:
            print(f"❌ Search Error: {e}")
            return []
        finally:
            conn.close()
