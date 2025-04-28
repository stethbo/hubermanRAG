import os
import chromadb
from openai import AzureOpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

PATH_TO_DB = "../db/chroma"
RAG_PROMPT = "You are an advanced AI assistant using retrieval-augmented generation to provide detailed and accurate responses. \
Use the following pieces of retrieved context from Andrew Huberman's teachings to answer the question. \
If you don't know the answer, say that you don't know.\n\n"

# setting up LLM
ENDPOINT = "https://26035-ma0waj70-eastus2.cognitiveservices.azure.com/"
MODEL_NAME = "gpt-4o-mini"
DEPLOYMENT = "gpt-4o-mini"
SUBSCRIPTION_KEY = os.getenv("AZURE_API_KEY")
API_VERSION = "2024-12-01-preview"

llm_client = AzureOpenAI(
    api_version=API_VERSION,
    azure_endpoint=ENDPOINT,
    api_key=SUBSCRIPTION_KEY,
)

class RAGService:
    def __init__(self):
        self.vector_store = self.initialize_vector_store()

    def initialize_vector_store(self):
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        chroma_client = chromadb.PersistentClient(path=PATH_TO_DB)
        vector_store = Chroma(
            embedding_function=embeddings,
            client=chroma_client,
            collection_name="huberman_lab"
        )
        return vector_store

    def get_top_docs_mmr(self, query, k=6, fetch_k=20, lambda_mult=0.5):
        return self.vector_store.max_marginal_relevance_search(
            query,
            k=k,
            fetch_k=fetch_k,
            lambda_mult=lambda_mult
        )

    def get_llm_response(self, question):
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

    def query_with_rag(self, user_input):
        retrieved_docs = self.get_top_docs_mmr(user_input)
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])
        query = f"{RAG_PROMPT}\nRetrieved information:\n {context}\n\nQuestion: {user_input}"
        return self.get_llm_response(query)

    def query_without_rag(self, user_input):
        return self.get_llm_response(user_input) 