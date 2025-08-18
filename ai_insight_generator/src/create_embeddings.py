import os
import sqlite3
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from tqdm import tqdm
from .database import get_db_connection

# --- Configuration ---
# These should be set as environment variables for security and flexibility.
# PINECONE_ENVIRONMENT is deprecated, but we keep it here for context.
# The environment is now part of the host name you get from app.pinecone.io
PINECONE_INDEX_NAME = "ai-reskilling-book"
MODEL_NAME = 'all-MiniLM-L6-v2' # A good, fast starting model

def fetch_chapters_from_db():
    """Fetches all chapters from the SQLite database."""
    print("Fetching chapters from the database...")
    conn = get_db_connection()
    # Ensure the Row factory is being used to get dict-like access
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content FROM chapters ORDER BY id")
    chapters = cursor.fetchall()
    conn.close()
    print(f"Found {len(chapters)} chapters.")
    return chapters

def generate_embeddings(chapters, model):
    """Generates vector embeddings for a list of chapters."""
    print("Generating embeddings for chapter content...")
    # We embed a combination of title and content for better semantic meaning
    chapter_texts = [f"Chapter: {ch['title']}\n\n{ch['content']}" for ch in chapters]
    embeddings = model.encode(chapter_texts, show_progress_bar=True, convert_to_tensor=False)
    return embeddings

def upsert_to_pinecone(index, chapters, embeddings):
    """Upserts the embeddings and metadata to the Pinecone index in batches."""
    print("Upserting vectors to Pinecone...")
    batch_size = 100 # Recommended batch size for Pinecone

    for i in tqdm(range(0, len(chapters), batch_size), desc="Upserting to Pinecone"):
        i_end = min(i + batch_size, len(chapters))

        # Prepare batch of vectors with metadata
        vectors_batch = []
        for j in range(i, i_end):
            chapter_id = chapters[j]['id']
            embedding = embeddings[j].tolist()
            # Metadata helps in filtering and provides context
            metadata = {"title": chapters[j]['title'], "content_preview": chapters[j]['content'][:250]}
            vectors_batch.append({
                "id": str(chapter_id),
                "values": embedding,
                "metadata": metadata
            })

        # Upsert batch
        index.upsert(vectors=vectors_batch)
    print("Upsert complete.")

def main():
    """Main function to run the embedding pipeline."""
    api_key = os.environ.get("PINECONE_API_KEY")
    if not api_key:
        print("Error: PINECONE_API_KEY environment variable not set.")
        print("Please set this environment variable before running the script.")
        return

    # 1. Fetch data
    chapters = fetch_chapters_from_db()
    if not chapters:
        print("No chapters found in the database. Please run the data parser first.")
        return

    # 2. Initialize models and clients
    print(f"Loading sentence-transformer model: {MODEL_NAME}...")
    model = SentenceTransformer(MODEL_NAME)

    print("Initializing Pinecone client...")
    pc = Pinecone(api_key=api_key)

    # 3. Create Pinecone index if it doesn't exist
    if PINECONE_INDEX_NAME not in pc.list_indexes().names():
        print(f"Creating new Pinecone index: {PINECONE_INDEX_NAME}...")
        # Serverless is cost-effective for development and scales well.
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=model.get_sentence_embedding_dimension(),
            metric='cosine',
            spec=ServerlessSpec(cloud='aws', region='us-west-2')
        )
        print("Index created.")

    index = pc.Index(PINECONE_INDEX_NAME)
    index.describe_index_stats() # Good practice to check index status

    # 4. Generate embeddings
    embeddings = generate_embeddings(chapters, model)

    # 5. Upsert to Pinecone
    upsert_to_pinecone(index, chapters, embeddings)

    print("\nEmbedding pipeline finished successfully!")
    index.describe_index_stats()

if __name__ == '__main__':
    main()
