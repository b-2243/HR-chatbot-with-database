import pyodbc
import pandas as pd
from sqlalchemy import create_engine,text
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle

SERVER = 'DESKTOP-HEB09TT\\SQLEXPRESS'
DATABASE = 'SkyHR'
DRIVER = 'ODBC Driver 17 for SQL Server'

engine = create_engine(
    f"mssql+pyodbc://@{SERVER}/{DATABASE}?trusted_connection=yes&driver={DRIVER.replace(' ', '+')}"
)

with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE'
    """))
    tables = [row[0] for row in result.fetchall()]

model = SentenceTransformer('all-MiniLM-L6-v2')
embedding_dim = 384


os.makedirs("faiss_store", exist_ok=True)

for table in tables:
    print(f"🔄 Processing table: {table}")
    try:
        df = pd.read_sql(f"SELECT * FROM {table}", engine)
        print("df",df)
        if df.empty:
            print(f"⚠️ Table {table} is empty. Skipping.")
            continue

        texts = df.astype(str).apply(lambda row: ', '.join(f"{col}: {val}" for col, val in row.items()), axis=1)
        print("texts",texts)
        embeddings = model.encode(texts.tolist(), show_progress_bar=True)
        embeddings = np.array(embeddings).astype('float32')

        index = faiss.IndexFlatL2(embedding_dim)
        index.add(embeddings)

        faiss.write_index(index, f"faiss_store/{table}_index.faiss")

        metadata = []
        for i, row_text in enumerate(texts):
            metadata.append({
                "table": table,
                "row_index": i,
                "row_text": row_text
            })

        with open(f"faiss_store/{table}_metadata.pkl", "wb") as f:
            pickle.dump(metadata, f)

        print(f"✅ Done processing table: {table}, stored {len(texts)} embeddings.")

    except Exception as e:
        print(f"❌ Error processing table {table}: {e}")
        continue

print("\n🎉 All embeddings created and stored successfully per table.")
