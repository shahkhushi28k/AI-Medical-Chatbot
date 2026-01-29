from flask import Flask, render_template, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import system_prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import os

app = Flask(__name__)
load_dotenv()

# ENV
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Embeddings (UNCHANGED)
embeddings = download_hugging_face_embeddings()

# Pinecone
index_name = "medical-chatbot"
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)

# Gemini LLM
from langchain_groq import ChatGroq

chatModel = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
    api_key=os.environ["GROQ_API_KEY"]
)


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}")
    ]
)

rag_chain = (
    {
        "context": retriever,
        "input": RunnablePassthrough()
    }
    | prompt
    | chatModel
    | StrOutputParser()
)

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/get", methods=["POST"])
def chat():
    msg = request.form["msg"]
    response = rag_chain.invoke(msg)
    return str(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
