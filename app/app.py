import os
import requests
import streamlit as st
import chromadb
from langchain.vectorstores import FAISS, Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.docstore.in_memory import InMemoryDocstore

from dotenv import load_dotenv
load_dotenv()


TOKEN = os.getenv("CLARIN_TOKEN")
CLARIN_CHAT_ENDPOINT = "https://services.clarin-pl.eu/api/v1/oapi/chat/completions"
MODEL_ID = "llama3.1"
PATH_TO_DB = "../db/chroma"
RAG_PROMPT = "You are an advanced AI assistant using retrieval-augmented generation to provide detailed and accurate responses. \
Use the following pieces of retrieved context from Andrew Huberman's teachings to answer the question. \
If you don't know the answer, say that you don't know.\n\n"


def initialize_vector_store():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    chroma_client = chromadb.PersistentClient(path=PATH_TO_DB)
    vector_store = Chroma(
        embedding_function=embeddings,
        client=chroma_client,
        collection_name="huberman_lab"
    )
    return vector_store


def get_top_docs(vector_store, query, k=6):
    return vector_store.similarity_search(query, k=k)


def get_llm_response(question):
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL_ID,
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    }
    response = requests.post(CLARIN_CHAT_ENDPOINT, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print("Response content:", response.text)
        return None


def generate_rag_response(vector_store, query):
    top_docs = get_top_docs(vector_store, query)
    context = "\n\n".join([doc.page_content for doc in top_docs])
    query = f"{RAG_PROMPT}\nRetrieved information:\n {context}\n\nQuestion: {query}"
    return get_llm_response(query)


vector_store = initialize_vector_store()
st.image("images/HUBLAB_banner.jpg", width=1000)
use_rag = st.toggle("Use RAG", value=True)
user_input = st.text_input("Ask a question about Dr. Huberman's teachings:", key="user_input")

if user_input:
    if use_rag:
        with st.spinner("Searching Huberman Lab knowledge base..."):
            retrieved_docs = get_top_docs(vector_store, user_input)
            context = "\n\n".join([doc.page_content for doc in retrieved_docs])

        with st.spinner("Generating response..."):
            response_text = generate_rag_response(vector_store, user_input)
            response = response_text['choices'][0]['message']['content']
    else:
        with st.spinner("Generating response..."):
            response_text = get_llm_response(user_input)
            response = response_text['choices'][0]['message']['content']

    st.write(response)