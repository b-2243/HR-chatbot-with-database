import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
embedding_dim = 384

index_dict = {}
metadata_dict = {}

faiss_dir = "faiss_store"

for file in os.listdir(faiss_dir):
    if file.endswith("_index.faiss"):
        table_name = file.replace("_index.faiss", "")
        index_path = os.path.join(faiss_dir, file)
        metadata_path = os.path.join(faiss_dir, f"{table_name}_metadata.pkl")

        index = faiss.read_index(index_path)

        with open(metadata_path, "rb") as f:
            metadata = pickle.load(f)

        index_dict[table_name] = index
        metadata_dict[table_name] = metadata

print(" All FAISS indexes and metadata loaded.")


def query_chatbot(user_query, top_k=10):
    print(f"\n Searching for: {user_query}")
    query_embedding = model.encode([user_query])[0].astype('float32')

    results = []

    for table, index in index_dict.items():
        D, I = index.search(np.array([query_embedding]), top_k)

        for i, score in zip(I[0], D[0]):
            if i == -1:
                continue
            row_info = metadata_dict[table][i]
            results.append((score, table, row_info["row_text"]))

    results.sort(key=lambda x: x[0])  

    if not results:
        return " No relevant data found."

    response = "\n Top Matches:\n"
    for i, (score, table, text) in enumerate(results[:top_k]):
        response += f"\n[{i+1}] (Table: {table}) → {text}"

    return response


if __name__ == "__main__":
    print("\n Simple RAG Chatbot (FAISS-Based) is ready!")
    print("Type your question (or type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print(" Goodbye!")
            break

        answer = query_chatbot(user_input)
        print(answer)
