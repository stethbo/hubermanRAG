import os
import requests
import streamlit as st
import chromadb
from openai import AzureOpenAI
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from firebase_config import firebase_config

from dotenv import load_dotenv
load_dotenv()

# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# Initialize Firebase Admin SDK (for Firestore)
try:
    app = firebase_admin.get_app()
except ValueError:
    # Path to your service account key JSON file - this provides access to all Firebase services
    cred = credentials.Certificate("hubermanrag-firebase-adminsdk-fbsvc-1fb326ddbd.json")
    app = firebase_admin.initialize_app(cred)

# Now get Firestore client
db = firestore.client()

# Streamlit session state for user
if "user" not in st.session_state:
    st.session_state.user = None


PATH_TO_DB = "../db/chroma"
RAG_PROMPT = "You are an advanced AI assistant using retrieval-augmented generation to provide detailed and accurate responses. \
Use the following pieces of retrieved context from Andrew Huberman's teachings to answer the question. \
If you don't know the answer, say that you don't know.\n\n"

# setting up LLM
ENDPOINT = "https://26035-ma0waj70-eastus2.cognitiveservices.azure.com/"
MODEL_NAME = "gpt-4o"
DEPLOYMENT = "gpt-4o"
SUBSCRIPTION_KEY = os.getenv("AZURE_API_KEY")
API_VERSION = "2024-12-01-preview"

llm_client = AzureOpenAI(
    api_version=API_VERSION,
    azure_endpoint=ENDPOINT,
    api_key=SUBSCRIPTION_KEY,
)



def initialize_vector_store():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    chroma_client = chromadb.PersistentClient(path=PATH_TO_DB)
    vector_store = Chroma(
        embedding_function=embeddings,
        client=chroma_client,
        collection_name="huberman_lab"
    )
    return vector_store


def get_top_docs_mmr(vector_store, query, k=6, fetch_k=20, lambda_mult=0.5):
    return vector_store.max_marginal_relevance_search(
        query,
        k=k,
        fetch_k=fetch_k,
        lambda_mult=lambda_mult
    )


def get_llm_response(question) -> str:
    response = llm_client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            },
            {
                "role": "user",
                "content": question,
            }
        ],
        max_tokens=4096,
        temperature=1.0,
        top_p=1.0,
        model=DEPLOYMENT
    )
    
    return response.choices[0].message.content


def login_signup():
    st.sidebar.title("Authentication")
    choice = st.sidebar.selectbox("Login/Signup", ["Login", "Signup"])
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")

    if choice == "Signup" and st.sidebar.button("Signup"):
        try:
            user = auth.create_user_with_email_and_password(email, password)
            st.session_state.user = user
            st.success("Account created!")
        except Exception as e:
            st.error(f"Error: {e}")
    elif choice == "Login" and st.sidebar.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state.user = user
            st.success("Logged in!")
        except Exception as e:
            st.error(f"Error: {e}")
    if st.sidebar.button("Logout") and st.session_state.user:
        st.session_state.user = None
        st.success("Logged out!")

def main():
    vector_store = initialize_vector_store()
    
    # Authentication
    login_signup()
    
    if not st.session_state.user:
        st.warning("Please log in to continue.")
        return

    st.image("app/images/HUBLAB_banner.jpg", width=1000)
    use_rag = st.toggle("Use RAG", value=True)
    
    # Get chat history from Firestore
    user_id = st.session_state.user["localId"]
    chat_history = db.collection("chats").document(user_id).get()
    if chat_history.exists:
        messages = chat_history.to_dict().get("messages", [])
    else:
        messages = []

    # Display chat history
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat input
    if user_input := st.chat_input("Ask a question about Dr. Huberman's teachings:"):
        # Add user message to Firestore
        messages.append({"role": "user", "content": user_input})
        db.collection("chats").document(user_id).set({"messages": messages})

        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            if use_rag:
                with st.spinner("Searching Huberman Lab knowledge base..."):
                    retrieved_docs = get_top_docs_mmr(vector_store, user_input)
                    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
                
                with st.spinner("Generating response..."):
                    query = f"{RAG_PROMPT}\nRetrieved information:\n {context}\n\nQuestion: {user_input}"
                    response = get_llm_response(query)
            else:
                with st.spinner("Generating response..."):
                    response = get_llm_response(user_input)

            st.write(response)
            
            # Add assistant response to Firestore
            messages.append({"role": "assistant", "content": response})
            db.collection("chats").document(user_id).set({"messages": messages})

if __name__ == "__main__":
    main()