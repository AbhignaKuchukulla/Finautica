from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

def setup_reflector():
    prompt = ChatPromptTemplate.from_template("""
    Analyze financial results:
    {results}
    
    Provide insights on:
    1. What worked well
    2. Improvement areas
    3. Suggested adjustments
    
    Format as JSON with keys: strengths, improvements, adjustments
    """)
    return prompt | Ollama(model="mixtral")

reflector = setup_reflector()
vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)