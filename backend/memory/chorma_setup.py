from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

def get_vector_db():
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5",
        model_kwargs={"device": "cpu"}
    )
    return Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )

def store_memory(text: str, metadata: dict, vector_db):
    vector_db.add_texts(
        texts=[text],
        metadatas=[metadata]
    )